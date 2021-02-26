gceimgutils
===========

A collection of utilities for image management in Google Compute Engine

While the functionality provided by the utilities is more or less a duplication
of functionality available with the gcloud CLI tools from the [google-cloud-sdk](https://cloud.google.com/sdk) the google-cloud-sdk does not provide consumable sources for packaging in a distribution nor is there a project for upstream contributions. This project focuses on image management only.

All utilities expect the service account credentials in ~/.config/gce. The name of the credentials file is expected to match the project name followed by the .json extension.

## Installation

### openSUSE and SUSE Linux Enterprise

```
> zypper in python3-gceimgutils
```

### PyPI

```
> pip install gceimgutils
```

## Utilities


### gcedeprecateimg - TBI
=======

A command line utility to deprecate images in GCE. 

The image set as the replacement is removed from the list of potential
images to be deprecated before any matching takes place. Therefore, the
deprecation search criteria specified with _--image-name-frag_ or
_--image-name-match_ cannot match the replacement image.

#### Usage

```
> gcedeprecateimg --project example --image-name-match v15 --replacement-name exampleimage_v16
```

See the [man pages](man/man1/gcedeprecateimg.1) for more information.

```
man gcedeprecateimg
```

### gcelistimg - TBI
=======

A command line utility to list the images in a project.

#### Usage

```
> gcelistimg --project example --image-name-frag foo
```

See the [man pages](man/man1/gcelistimg.1) for more information.

```
man gcelistimg
```

### gceremoveimg

A command line utility to remove images in GCE.

#### Usage

```
> gceremoveimg --project example --image-name-match v15
```

See the [man pages](man/man1/gceuploadimg.1) for more information.

```
man gceremoveimg
```

