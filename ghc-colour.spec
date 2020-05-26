#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	colour
Summary:	A model for human colour/color perception
Name:		ghc-%{pkgname}
Version:	2.3.5
Release:	1
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/colour
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	fe7bbf4c511d5ad8b626caf53c544682
URL:		http://hackage.haskell.org/package/colour
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.9
BuildRequires:	ghc-QuickCheck >= 2.5
BuildRequires:	ghc-random >= 1.0
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base-prof >= 4.9
BuildRequires:	ghc-QuickCheck-prof >= 2.5
BuildRequires:	ghc-random-prof >= 1.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-base >= 4.9
Requires:	ghc-QuickCheck >= 2.5
Requires:	ghc-random >= 1.0
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package provides a data type for colours and transparency.
Colours can be blended and composed. Various colour spaces are
supported. A module of colour names (Data.Colour.Names) is provided.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-prof
Requires:	ghc-base-prof >= 4.9
Requires:	ghc-QuickCheck-prof >= 2.5
Requires:	ghc-random-prof >= 1.0

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README %{name}-%{version}-doc/html
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/CIE
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/CIE/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/CIE/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/RGBSpace
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/RGBSpace/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/RGBSpace/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/SRGB
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/SRGB/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/SRGB/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/CIE/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/RGBSpace/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Colour/SRGB/*.p_hi
%endif
