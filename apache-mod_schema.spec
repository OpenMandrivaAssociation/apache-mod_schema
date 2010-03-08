#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_schema
%define mod_conf B35_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Schema handler module
Name:		apache-%{mod_name}
Version:	0.1.7
Release:	%mkrel 6
Group:		System/Servers
License:	LGPL
URL:		http://sourceforge.net/projects/modschema
Source0:	%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
Requires:	apache-mod_apreq >= 2.08
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	glib2-devel
BuildRequires:	libapreq-devel >= 2.08
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_schema is an Apache module which allows instance XML document validations
with the W3C schema language. The validation is based on Xerces C++ library and
the module enables a Web tool for multi schema validations.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build

%configure2_5x --localstatedir=/var/lib

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc forms COPYING README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

