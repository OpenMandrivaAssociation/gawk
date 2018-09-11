%bcond_with crosscompile
%define __noautoprov '.*\\.so(.*)'

Summary:	The GNU version of the awk text processing utility
Name:		gawk
Version:	4.2.1
Release:	3
License:	GPLv3+
Group:		Text tools
Url:		http://www.gnu.org/software/gawk/gawk.html
Source0:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.xz
# (tpg) patches from upstream
Patch000:	gawk-4.2.1-000-add-support-for-a-and-A-in-printf.patch
Patch001:	gawk-4.2.1-001-remove-the-tail-recursion-optimization.patch
Patch002:	gawk-4.2.1-002-copy-MPZ-MPFR-bits-also-in-r_dupnode.patch
Patch003:	gawk-4.2.1-003-fix-rebuilding-records-if-using-API-parser.patch
Patch004:	gawk-4.2.1-004-fix-a-corner-case-with-EPIPE-to-stdout-stderr.patch
BuildRequires:	byacc
BuildRequires:	gettext-devel
BuildRequires:	libsigsegv-devel >= 2.8
BuildRequires:	mpfr-devel
BuildRequires:	gmp-devel
BuildRequires:	readline-devel >= 7.0
BuildRequires:	autoconf-archive
# For building docs
BuildRequires:	texlive-epsf
BuildRequires:	texlive
BuildRequires:	texinfo
BuildRequires:	texlive-dvips
BuildRequires:	texlive-collection-latex
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
%define _disable_rebuild_configure 1

%configure \
%if %{with crosscompile}
	--with-libsigsegv-prefix=no
%else
	--with-libsigsegv-prefix=%{_prefix}
%endif

%make_build
%make_build -C doc

# (tpg) seems like tests fails due to overlayfs which is used inside docker-builder
#check
#make check

%install
%make_install  bindir=/bin
%find_lang %{name}

mkdir -p %{buildroot}%{_bindir}
cd %{buildroot}%{_datadir}
mkdir awk && for i in *.awk;do
	mv $i awk
done
cd %{buildroot}%{_mandir}/man1
ln -s gawk.1 awk.1
cd %{buildroot}%{_bindir}
ln -s ../../bin/awk %{buildroot}%{_bindir}/awk
ln -s ../../bin/gawk %{buildroot}%{_bindir}/gawk
rm %{buildroot}/bin/gawk-%{version}

# For now, there's nothing that uses the gawk API.
# Let's start shipping it if and when it becomes useful.
rm -rf %buildroot%_includedir

%files -f %{name}.lang
/bin/*
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/*/*
%{_infodir}/*
%{_libdir}/gawk
%{_datadir}/awk
%{_sysconfdir}/profile.d/gawk.*

%files doc
%doc README INSTALL NEWS
%doc README_d POSIX.STD doc/*.pdf
