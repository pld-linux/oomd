%bcond_without tests

Summary:	Userspace Out-Of-Memory (OOM) killer
Name:		oomd
Version:	0.5.0
Release:	0.1
License:	GPL v2
URL:		https://github.com/facebookincubator/oomd/
Source0:	https://github.com/facebookincubator/oomd/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9fe50e737e6c6a638effe05d8d12aeda
# Check return value for mkstemp()
Patch0:		https://github.com/facebookincubator/oomd/commit/076af42b270388f38055fdf60dccbb3001de723a.patch
# Patch0-md5:	a3171e3a39e5429381b3edf9268df5e9
# Fix ODR violation in tests
Patch1:		https://github.com/facebookincubator/oomd/commit/3989e169fc0da9c29da8dd692427d4f4c1ace413.patch
# Patch1-md5:	5fbe5ad8057d3b511bcdaa2a1ffff734
# Resolved a compiler error due to lacking include
Patch2:		https://github.com/facebookincubator/oomd/commit/83a6742f08349fbc93f459228dcc3d1f56eac411.patch
# Patch2-md5:	111dbaae2a16f7a747a431e0c1425753

BuildRequires:	jsoncpp-devel
BuildRequires:	meson >= 0.45
BuildRequires:	systemd-devel
%if %{with tests}
BuildRequires:	gmock-devel
BuildRequires:	gtest-devel
%endif
ExcludeArch:	i686 armv7hl

%description
Out of memory killing has historically happened inside kernel space.
On a memory overcommitted linux system, malloc(2) and friends usually
never fail. However, if an application dereferences the returned
pointer and the system has run out of physical memory, the linux
kernel is forced take extreme measures, up to and including killing
processes. This is sometimes a slow and painful process because the
kernel can spend an unbounded amount of time swapping in and out pages
and evicting the page cache. Furthermore, configuring policy is not
very flexible while being somewhat complicated.

oomd aims to solve this problem in userspace. oomd leverages PSI and
cgroupv2 to monitor a system holistically. oomd then takes corrective
action in userspace before an OOM occurs in kernel space. Corrective
action is configured via a flexible plugin system, in which custom
code can be written. By default, this involves killing offending
processes. This enables an unparalleled level of flexibility where
each workload can have custom protection rules. Furthermore, time
spent livedlocked in kernelspace is minimized.

%prep
%setup -q

%build
%meson
%meson_build

%if %{with tests}
%check
%meson_test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post oomd.service

%preun
%systemd_preun oomd.service

%postun
%systemd_postun_with_restart oomd.service

%files
%defattr(644,root,root,755)
%doc README.md CONTRIBUTING.md CODE_OF_CONDUCT.md docs/
%attr(755,root,root) %{_bindir}/oomd
%{systemdunitdir}/oomd.service
%{_mandir}/man1/oomd.*
%config(noreplace) %{_sysconfdir}/oomd/
