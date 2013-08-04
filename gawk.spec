%bcond_with crosscompile
%define __noautoprov '.*\\.so(.*)'

Summary:	The GNU version of the awk text processing utility
Name:		gawk
Version:	4.1.0
Release:	8
License:	GPLv3+
Group:		Text tools
Url:		http://www.gnu.org/software/gawk/gawk.html
Source0:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.xz
Source1:	http://ftp.gnu.org/gnu/gawk/%{name}-3.1.6-ps.tar.gz
BuildRequires:	byacc
BuildRequires:	gettext-devel
BuildRequires:	libsigsegv-devel >= 2.8
Provides:	awk

%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.

%package	doc
Summary:	Documentation about the GNU version of the awk text processing utility
Group:		Books/Computer books

%description	doc
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.

%prep
%setup -q -b 1
mv ../%{name}-3.1.6/doc/*.ps doc
rm -rf ../%{name}-3.1.6

%build
%configure2_5x \
%if %{with crosscompile}
	--with-libsigsegv-prefix=no
%else
	--with-libsigsegv-prefix=%{_prefix}
%endif

%make

%check
make check

%install
%makeinstall_std  bindir=/bin
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
%{_mandir}/*/*
%{_infodir}/*
%{_libdir}/awk
%{_libdir}/gawk
%{_datadir}/awk

%files doc
%doc README INSTALL NEWS
%doc README_d POSIX.STD doc/*.ps
