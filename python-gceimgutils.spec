#
# spec file for package python-gceimgutils
#
# Copyright (c) 2018 SUSE Linux GmbH, Nuernberg, Germany.
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
%define python python
%{?sle15_python_module_pythons}

%if 0%{?suse_version} > 1500
%bcond_without libalternatives
%else
%bcond_with libalternatives
%endif

Name:           python-gceimgutils
Version:        0.13.0
Release:        0
Summary:        Image management utilities for GCE
License:        GPL-3.0+
Group:          System/Management
Url:            https://github.com/SUSE-Enceladus/gceimgutils
Source0:        %{upstream_name}-%{version}.tar.bz2
Requires:       python
Requires:       python-google-auth
Requires:       python-google-cloud-compute
Requires:       python-google-cloud-core
Requires:       python-google-cloud-storage
BuildRequires:  %{python_module google-auth}
BuildRequires:  %{python_module google-cloud-compute}
BuildRequires:  %{python_module google-cloud-core}
BuildRequires:  %{python_module google-cloud-storage}
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module wheel}
BuildRequires:  python-rpm-macros
Provides:       python3-gceimgutils = %{version}
Obsoletes:      python3-gceimgutils < %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%if %{with libalternatives}
BuildRequires:  alts
Requires:       alts
%else
Requires(post): update-alternatives
Requires(postun): update-alternatives
%endif

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
%python_clone -a %{buildroot}%{_bindir}/gceremoveimg
%python_clone -a %{buildroot}%{_bindir}/gcelistimg


%pre
%python_libalternatives_reset_alternative gceremoveimg
%python_libalternatives_reset_alternative gcelistimg

%post
%{python_install_alternative gceremoveimg}
%{python_install_alternative gcelistimg}

%postun
%{python_uninstall_alternative gceremoveimg}
%{python_uninstall_alternative gcelistimg}

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_mandir}/man*/*
%dir %{python_sitelib}/gceimgutils
%{python_sitelib}/*
%python_alternative %{_bindir}/gceremoveimg
%python_alternative %{_bindir}/gcelistimg

%changelog
