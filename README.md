# boxpy
boxpy is a utility for manipulating contents stored in box.com

## usage

boxpy -f cfg --overwrite SRC_FILE FOO/BAR/DST_FILE_NAME

The -f cfg flag is mandatory, which stores your account credential. boxpy is not able to upload file without these information. The content of cfg file is:
```
cfg file content goes here
```

boxpy will refuse to upload file if the  if the dst file already exists, unless --overwrite flag is given.
