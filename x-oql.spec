%define gcj_support 1

%define	name	x-oql
%define	oname	X-OQL
%define	jarname	xoql
%define	version	20070202
%define	release	%mkrel 4
%define	jarlibs	cdqa antlr

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{oname}
License:	LGPL
Group:		Development/Java
Url:		http://forge.objectweb.org/projects/activexml/
# from cvs
Source0:	%{name}-%{version}.tar.lzma
BuildRequires:	lzma
BuildRequires:	java-rpmbuild java-devel ant %{jarlibs}
Requires:	%{jarlibs}
Provides:	%{oname} = %{version}-%{release}
Provides:	%{jarname} = %{version}-%{release}
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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


