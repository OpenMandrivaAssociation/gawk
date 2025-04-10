%bcond_with crosscompile
%define _disable_rebuild_configure 1
%define __provides_exclude '.*\\.so(.*)'
%global optflags %{optflags} -Oz

Summary:	The GNU version of the awk text processing utility
Name:		gawk
Version:	5.3.2
Release:	1
License:	GPLv3+
Group:		Text tools
Url:		https://www.gnu.org/software/gawk/gawk.html
Source0:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.xz
Patch0:		gawk-5.1.0-no-Lusrlib.patch
Patch1:		gawk-5.1.0-fix-clang.patch

BuildRequires:	byacc
BuildRequires:	gettext-devel
BuildRequires:	libsigsegv-devel >= 2.8
BuildRequires:	pkgconfig(mpfr)
BuildRequires:	pkgconfig(gmp)
BuildRequires:	pkgconfig(readline)
BuildRequires:	slibtool
BuildRequires:	autoconf-archive
# For building docs
BuildRequires:	texinfo
BuildRequires:	groff
# This allows some locale specific tests to pass
BuildRequires:	locales-en
Provides:	awk
# do not remove, it's needed in synthesis which doesn't contain file paths,
# which again rpm may auto generate provides against
Provides:	/bin/awk
Provides:	/usr/bin/awk

%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.

%package doc
Summary:	Documentation about the GNU version of the awk text processing utility
Group:		Books/Computer books

%description doc
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.

%prep
%autosetup -p1

# bug with tests
sed -i '/^pty1:$/s|$|\n_pty1:|' test/Makefile.in

%build
cd extension
slibtoolize --force
aclocal -I ../m4
autoheader
automake -a
autoconf
cd ..

slibtoolize --force
aclocal -I m4
autoheader
automake -a
autoconf

%configure \
%if %{with crosscompile}
	--with-libsigsegv-prefix=no
%else
	--with-libsigsegv-prefix=%{_prefix}
%endif

%make_build \
%if %{cross_compiling}
	AWK=%{_bindir}/gawk \
%endif
	AR=llvm-ar \
	RANLIB=llvm-ranlib
%make_build -C doc

# (tpg) seems like tests fails due to overlayfs which is used inside docker-builder
#check
#make check

%install
%make_install
%find_lang %{name}


cd %{buildroot}%{_datadir}
mkdir awk && for i in *.awk;do
    mv $i awk
done
cd %{buildroot}%{_mandir}/man1
ln -s gawk.1 awk.1

rm %{buildroot}/%{_bindir}/gawk-%{version}

# For now, there's nothing that uses the gawk API.
# Let's start shipping it if and when it becomes useful.
rm -rf %{buildroot}%{_includedir}

%files -f %{name}.lang
%{_bindir}/*
%{_libexecdir}/*
%doc %{_mandir}/*/*
%doc %{_infodir}/*
%{_libdir}/gawk
%{_datadir}/awk
%{_sysconfdir}/profile.d/gawk.*

%files doc
%doc README INSTALL NEWS
%doc README_d POSIX.STD doc/*.pdf
