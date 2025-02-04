%define gcj_support 1

%define	name	x-oql
%define	oname	X-OQL
%define	jarname	xoql
%define	version	20070202
%define release	10
%define	jarlibs	cdqa antlr

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{oname}
License:	LGPL
Group:		Development/Java
Url:		https://forge.objectweb.org/projects/activexml/
# from cvs
Source0:	%{name}-%{version}.tar.lzma
BuildRequires:	lzma
BuildRequires:	java-rpmbuild java-devel ant %{jarlibs}
BuildRequires:	locales-en
Requires:	%{jarlibs}
Provides:	%{oname} = %{version}-%{release}
Provides:	%{jarname} = %{version}-%{release}
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
%{oname}

%package	javadoc
Summary:	Javadoc for %{oname}
Group:		Development/Java

%description	javadoc
Javadoc for %{oname}.

%prep
%setup -q -n %{oname}
#make sure that we don't use precompiled java package if shipped
rm -rf lib

%build
export LC_ALL=ISO-8859-1
export CLASSPATH=$(build-classpath %{jarlibs})
%{ant} -f xoql_build.xml jar javadoc -DDSTAMP=%{version} 
jar -i build/lib/%{jarname}.jar

%install
rm -rf %{buildroot}


install -d %{buildroot}%{_javadir}
install -m644 build/lib/%{jarname}.jar -D %{buildroot}%{_javadir}/%{jarname}-%{version}.jar

for jarname in \
	%{buildroot}%{_javadir}/%{jarname}.jar \
	%{buildroot}%{_javadir}/%{name}{,-%{version}}.jar \
	%{buildroot}%{_javadir}/%{oname}{,-%{version}}.jar
do ln -s %{jarname}-%{version}.jar $jarname
done

install -d %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -r build/api %{buildroot}%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}




%changelog
* Wed Sep 09 2009 Thierry Vignaud <tvignaud@mandriva.com> 20070202-8mdv2010.0
+ Revision: 435251
- rebuild

* Mon Aug 04 2008 Thierry Vignaud <tvignaud@mandriva.com> 20070202-7mdv2009.0
+ Revision: 262644
- rebuild

* Thu Jul 31 2008 Thierry Vignaud <tvignaud@mandriva.com> 20070202-6mdv2009.0
+ Revision: 257626
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 20070202-4mdv2008.1
+ Revision: 121057
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 20070202-3mdv2008.0
+ Revision: 87304
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 20070202-2mdv2008.0
+ Revision: 82859
- rebuild


* Sat Feb 03 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 20070202-1mdv2007.0
+ Revision: 116045
- fix permissions for gcj libraries
- Import x-oql

