#
# spec file for package python-gceimgutils
#
# Copyright (c) 2025 SUSE LLC.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define upstream_name gceimgutils
%if 0%{?suse_version} >= 1600
%define pythons %{primary_python}
%else
%{?sle15_python_module_pythons}
%endif
%global _sitelibdir %{%{pythons}_sitelib}

Name:           python-gceimgutils
Version:        1.0.0
Release:        0
Summary:        Image management utilities for GCE
License:        GPL-3.0+
Group:          System/Management
Url:            https://github.com/SUSE-Enceladus/gceimgutils
Source0:        %{upstream_name}-%{version}.tar.bz2
Requires:       %{pythons}-google-auth
Requires:       %{pythons}-google-cloud-compute
Requires:       %{pythons}-google-cloud-core
Requires:       %{pythons}-google-cloud-storage
Requires:       %{pythons}-python-dateutil
BuildRequires:  %{pythons}-google-auth
BuildRequires:  %{pythons}-google-cloud-compute
BuildRequires:  %{pythons}-google-cloud-core
BuildRequires:  %{pythons}-google-cloud-storage
BuildRequires:  %{pythons}-pip
BuildRequires:  %{pythons}-setuptools
BuildRequires:  %{pythons}-wheel
BuildRequires:  %{pythons}-python-dateutil
BuildRequires:  python-rpm-macros
BuildRequires:  fdupes
Provides:       python3-gceimgutils = %{version}
Obsoletes:      python3-gceimgutils < %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
A collection of image manipulation utilities for GCE. These include:
gceremoveimg: Removes images from GCE

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
install -d -m 755 %{buildroot}/%{_mandir}/man1
install -m 644 man/man1/* %{buildroot}/%{_mandir}/man1
gzip %{buildroot}/%{_mandir}/man1/*
%python_expand %fdupes %{buildroot}%{_sitelibdir}

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_mandir}/man*/*
%dir %{_sitelibdir}/gceimgutils
%{_sitelibdir}/gceimgutils/*
%{_sitelibdir}/gceimgutils-*.dist-info/
%{_bindir}/gceremoveimg
%{_bindir}/gcelistimg
%{_bindir}/gcecreateimg
%{_bindir}/gcedeprecateimg
%{_bindir}/gceremoveblob
%{_bindir}/gceuploadblob

%changelog
