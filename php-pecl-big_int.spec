%define		_modname	big_int
%define		_status		stable
Summary:	%{_modname} - set of functions for calculations with arbitrary length integers
Summary(pl.UTF-8):   %{_modname} - zestaw funkcji do obliczeń z użyciem liczb o dowolnej wielkości
Name:		php-pecl-%{_modname}
Version:	1.0.7
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	d858d5bcfd3f789cb1ae8cb8ff09d3e9
URL:		http://pecl.php.net/package/big_int/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package is useful for number theory applications. For example, in
two-keys cryptography. See tests/RSA.php in the package for example of
implementation of RSA-like cryptoalgorithm.

Also the package has many bitset functions, which allow to work with
arbitrary length bitsets.

This package is much faster than bundled into PHP BCMath. It
implements almost all functions as in GMP extension, but it needn't
any additional external libraries.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Ten pakiet jest przydatny do zastosowań z teorii liczb, na przykład do
kryptografii z użyciem dwóch kluczy. Przykładową implementację
algorytmu kryptograficznego podobnego do RSA można znaleźć w tym
pakiecie w pliku tests/RSA.php.

Pakiet ma także wiele funkcji operujących na bitach, umożliwiających
działanie na zbiorach bitów dowolnej długości.

Ten pakiet jest dużo szybszy niż wbudowany w PHP BCMath. Implementuje
prawie wszystkie funkcje z rozszerzenia GMP, ale nie wymaga żadnych
dodatkowych bibliotek zewnętrznych.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{docs,tests,CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
