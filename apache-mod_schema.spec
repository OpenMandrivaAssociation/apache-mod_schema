#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_schema
%define mod_conf B35_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Schema handler module
Name:		apache-%{mod_name}
Version:	0.1.8
Release:	6
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



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.8-5mdv2012.0
+ Revision: 772758
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.8-4
+ Revision: 678412
- mass rebuild

* Thu Dec 02 2010 Paulo Andrade <pcpa@mandriva.com.br> 0.1.8-3mdv2011.0
+ Revision: 605245
- Rebuild with apr with workaround to issue with gcc type based

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.8-2mdv2011.0
+ Revision: 588058
- rebuild

* Sun Oct 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.8-1mdv2011.0
+ Revision: 586383
- 0.1.8

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-6mdv2010.1
+ Revision: 516174
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-5mdv2010.0
+ Revision: 406644
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-4mdv2009.1
+ Revision: 326231
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-3mdv2009.0
+ Revision: 235081
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-2mdv2009.0
+ Revision: 215630
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Tue May 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-1mdv2009.0
+ Revision: 202078
- import apache-mod_schema


* Tue May 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-1mdv2009.0
- initial Mandriva package
