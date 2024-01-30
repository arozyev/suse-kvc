#
# spec file for package suse-kvc
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
Name:             suse-kvc
Version:          1.0.1
Release:          0
Summary:          SUSE Kernel Version Checker
License:          MIT
URL:              https://github.com/arozyev/suse-kvc
Source:           %{name}-%{version}.tar.gz
Group:            Development/Languages/Python

BuildRequires:    python3-devel
BuildRequires:    python3-lxml
BuildRequires:    python3-requests
Requires:         python3-lxml
Requires:         python3-requests

%description
A simple python script that checks if given kernel up-to-date, if not, then it
will show how many new kernel versions have been released.

%prep
%setup -q

%build
# Nothing to do here

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 suse-kvc %{buildroot}%{_bindir}


%files
%defattr(-,root,root)
# %doc README.md
%{_bindir}/suse-kvc


%changelog
