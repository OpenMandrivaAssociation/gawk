Summary:	The GNU version of the awk text processing utility
Name:		gawk
Version:	3.1.6
Release:	%mkrel 4
License:	GPLv3+
Group:		Text tools
URL:		http://www.gnu.org/software/gawk/gawk.html
Source0:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.bz2
Source1:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}-ps.tar.gz
Patch0:		gawk-3.1.3-getpgrp_void.patch
Provides:	awk
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	byacc
Requires(pre):	info-install

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
%patch0 -p1 -b .getpgrp_void

%build
%configure2_5x
%make

%check
%make check

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std  bindir=/bin
%find_lang %{name}

rm %{buildroot}%{_infodir}/dir
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
mv %{buildroot}/bin/pgawk %{buildroot}%{_bindir}
rm %{buildroot}/bin/pgawk-%{version}

%post
%_install_info gawk.info

%preun
%_remove_install_info gawk.info

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) /bin/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*
%{_libdir}/awk
%{_datadir}/awk

%files doc
%defattr(-,root,root)
%doc README FUTURES INSTALL LIMITATIONS NEWS
%doc README_d POSIX.STD doc/gawk.ps doc/awkcard.ps


