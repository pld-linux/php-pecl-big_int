%define		_modname	big_int
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - set of functions for calculations with arbitrary length integers
Summary(pl):	%{_modname} - zestaw funkcji do obliczeñ z u¿yciem liczb o dowolnej wielko¶ci
Name:		php-pecl-%{_modname}
Version:	1.0.6
Release:	3
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	844332ab0a40ea12aa8339d7d2c20770
URL:		http://pecl.php.net/package/big_int/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
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

%description -l pl
Ten pakiet jest przydatny do zastosowañ z teorii liczb, na przyk³ad do
kryptografii z u¿yciem dwóch kluczy. Przyk³adow± implementacjê
algorytmu kryptograficznego podobnego do RSA mo¿na znale¼æ w tym
pakiecie w pliku tests/RSA.php.

Pakiet ma tak¿e wiele funkcji operuj±cych na bitach, umo¿liwiaj±cych
dzia³anie na zbiorach bitów dowolnej d³ugo¶ci.

Ten pakiet jest du¿o szybszy ni¿ wbudowany w PHP BCMath. Implementuje
prawie wszystkie funkcje z rozszerzenia GMP, ale nie wymaga ¿adnych
dodatkowych bibliotek zewnêtrznych.

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{docs,tests,CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
