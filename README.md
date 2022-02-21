# safe_imagefield
a django app that subclasses imagefield and that validates images in a number of ways.  It is a fork of safefilefield by vladislav bakin https://pypi.org/project/django-safe-filefield/

## validators
* FileExtensionValidator - validates file to check that its extension matches a list of allowed extensions.
                           pass the list of extensions when you add the validator
* FileContentTypeValidator - validates the content of the file against its guessed type and its extension.
* AntiVirusValidator - scans the file with clamav.  settings.CLAMAV_SOCKET specifies the webaddress or socket 
                       that clamav is on eg 'tcp://127.0.0.1:3310'.  settings.CLAMAV_TIMEOUT specifies a maximum amount of time before the scan times out.
* MediaIntegrityValidator - runs a few simple checks to confirm that the integrity of the file is good.  You can pass 'error_detect' as 'default' or 'strict' to the constructor.  Defaults to default.  Strict is a stricter check.
* MaxSizeValidator - validates the file size against a max_size of bytes.

This app is still being tested, so I can't give any guarantees as to its effectiveness.  Tests are untested currently.

Todo - add image files for tests.