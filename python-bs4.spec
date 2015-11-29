#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	bs4
Summary:	beautifulsoup4 - Screen-scraping library
Name:		python-%{module}
Version:	4.4.1
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/b/beautifulsoup4/beautifulsoup4-%{version}.tar.gz
# Source0-md5:	8fbd9a7cac0704645fa20d1419036815
Patch0:		test_suite.patch
URL:		http://www.crummy.com/software/BeautifulSoup/bs4/
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Beautiful Soup sits atop an HTML or XML parser, providing Pythonic
idioms for iterating, searching, and modifying the parse tree.

%package -n python3-%{module}
Summary:	beautifulsoup4 - Screen-scraping library
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Beautiful Soup sits atop an HTML or XML parser, providing Pythonic
idioms for iterating, searching, and modifying the parse tree.

%prep
%setup -q -n beautifulsoup4-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc {AUTHORS,NEWS,README,TODO}.txt
%{py_sitescriptdir}/bs4
%{py_sitescriptdir}/beautifulsoup4-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc {AUTHORS,NEWS,README,TODO}.txt
%{py3_sitescriptdir}/bs4
%{py3_sitescriptdir}/beautifulsoup4-%{version}-py*.egg-info
%endif
