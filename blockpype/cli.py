import argparse
import subprocess, sys


def setup_args():
    """Sets up command line parameters
    """
    parser = argparse.ArgumentParser(
        description="Breaks apart input stream into blocks and pipes each block into newly spawned processes.")

    command_group = parser.add_mutually_exclusive_group(required=True)

    command_group.add_argument(
        '-l',
        '--lines',
        help="Break apart after each LINES",
        type=int,
        default=None
    )

    command_group.add_argument(
        '-b',
        '--bytes',
        help="Break apart after each BYTES",
        type=int,
        default=None
    )

    command_group.add_argument(
        '-c',
        '--chars',
        help="Break apart after each CHARS",
        type=int,
        default=None
    )

    parser.add_argument(
        '--debug',
        action="store_true",
        help='Output debug information to stdout'
    )

    parser.add_argument('pipe_args', type=str, nargs='+', help='Process to start and pipe to')

    return parser.parse_known_args()


def endproc(proc: subprocess.Popen):
    """Properly ends a process and handles any errors
    """
    proc.communicate()
    code = proc.poll()
    if code is None:
        code = proc.wait()
    if code != 0:
        exit(code)


def main():
    """Entry point for CLI
    """
    args, unknownargs = setup_args()
    encoding = sys.stdin.encoding
    stream = None
    
    if args.chars:
        # Treat chars differently because we split on dynamic char length
        stream = sys.stdin
    else:
        # Treat everything else as a byte stream
        stream = sys.stdin.buffer

    # Enter only when input is present
    if not sys.stdin.isatty():
        proc = None
        if args.lines:
            # Process line by line
            lines = 0
            for line in stream:
                if lines == 0:
                    if args.debug:
                        print("blockpype > Starting process:")
                        print("blockpype > " + " ".join(args.pipe_args + unknownargs))
                        print("")
                    # Open a process only at start of block
                    proc = subprocess.Popen(args.pipe_args + unknownargs, stdin=subprocess.PIPE)

                # Write to process
                proc.stdin.write(line)
                lines += 1

                # Block is full. Finish writing to this process and end it
                if lines == args.lines:
                    if proc:
                        endproc(proc)
                        proc = None
                    if args.debug:
                        print(f"blockpype > Finished data block. Written {lines} lines to process. Ending process.")
                    lines = 0

            if proc:
                if args.debug:
                    print(f"blockpype > Finished input data. Written {lines} lines to process. Ending process.")
                endproc(proc)

        elif args.chars or args.bytes:
            # process buffer by buffer
            block_size = args.chars or args.bytes
            have_read = 0
            buff_size = 10000
            while True:
                if have_read == 0:
                    if args.debug:
                        print("blockpype > Starting process:")
                        print("blockpype > " + " ".join(args.pipe_args + unknownargs))
                        print("")
                    # Open a process only at start of block
                    proc = subprocess.Popen(args.pipe_args + unknownargs, stdin=subprocess.PIPE)

                buff = stream.read(min([buff_size, block_size - have_read]))
                len_buff = len(buff)
                if len_buff == 0:
                    if args.debug:
                        print(f"blockpype > Zero bytes in input. Ending.")
                    if proc:
                        endproc(proc)
                        proc = None
                    break

                # Write to process
                if args.chars:
                    proc.stdin.write(buff.encode(encoding))
                else:
                    proc.stdin.write(buff)
                have_read += len_buff

                # Block is full. Finish writing to this process and end it
                if block_size == have_read:
                    if args.debug:
                        print(f"blockpype > Finished data block. Written {have_read} bytes or chars to process. Ending process.")
                    have_read = 0
                    if proc:
                        endproc(proc)
                        proc = None

if __name__ == '__main__':
    main()
