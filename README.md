# Blockpype

Breaks apart input stream into blocks and pipes each block into newly spawned processes

## Installing

```
pip install git+https://github.com/kfzteile24/blockpype.git
```

## Testing
Clone the repository and run visual tests that display each started PID and their output:
* `test/by-byte.sh` - should break apart in the middle of the 2-byte character
* `test/by-char.sh` - should break apart in the middle of some numbers
* `test/by-line.sh` - should break apart nicely line by line

## Usage
```
cat content.txt | blockpype -l 10 other-program --arg-for-program --another-arg "argument value"
```

It will cut `content.txt` into blocks of 10 lines, and for each block, a process will be started using the command:

```
other-program --arg-for-program --another-arg "argument value"
```

and the contents of the block will be served to *stdin*

## What's it for?

Whenever you want to break apart a large stream when the `other-program` consumer stores it into memory until EOF, and you don't have enough memory for it.

Similar to `split --filter "other-program --arg-for-program --another-arg \"argument value\""` except less clunky, `other-program` gets launched from current `pwd` with the current user, and with the current environment variables.
