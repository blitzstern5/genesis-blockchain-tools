## 0.3.1 (2019-Jul-15 01:30)

* Fixed issues in find_mime_type_recursive function
* Added support of an object with mime_type attribute searching. Add more test cases
* Added support of an object with mime_type attribute searching
* Replaced EllipticCurvePublicNumbers.from_encoded_point with ec.EllipticCurvePublicNumbers.from_encoded_point
* Added python version agnostic load_module_by_path function to load module by path
* Freeze packages versions
* Update setup.py and add setup.cfg
* Added entry point for console script genbc-conv

## 0.3.0 (2019-May-19 20:58)

* Added genbc-conv cli utility to convert Key ID, Address, Private and Public Keys

## 0.2.1 (2018-Dec-26 18:44)

* Added several encoding/decoding functions duplicating its backend's versions
* Fixed many bugs in crypto backends
* Added functionality to create and sign client-side transactions

## 0.1.4 (2018-Jul-20 07:03)

* Added missing functionality to all backends: verify function
* Added crypto backends errors
* Added cross backends tests
* Some backend's common functions were moved to dedicated common module. Also tests for them were also added
* Fixed some bugs in misc backends
* Crypto backends were refactored and completed: missing verify functions were add
* Specific backends tests were added
* Old code was removed
