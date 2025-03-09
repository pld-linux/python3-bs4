#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	bs4
Summary:	beautifulsoup4 - Screen-scraping library
Summary(pl.UTF-8):	beautifulsoup4 - biblioteka przechwytująca wyjście
Name:		python-%{module}
# keep 4.9.x here for python2 support
Version:	4.9.3
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/beautifulsoup4/
Source0:	https://files.pythonhosted.org/packages/source/b/beautifulsoup4/beautifulsoup4-%{version}.tar.gz
# Source0-md5:	57fd468ae3eb055f6871106e8f7813e2
Patch0:		test_suite.patch
Patch2:		%{name}-smart_quotes.patch
URL:		https://www.crummy.com/software/BeautifulSoup/
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-soupsieve >= 1.2
%endif
%if %{with python3}
BuildRequires:	python3-2to3 >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
BuildRequires:	python3-soupsieve >= 1.2
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Beautiful Soup sits atop an HTML or XML parser, providing Pythonic
idioms for iterating, searching, and modifying the parse tree.

%description -l pl.UTF-8
Beautiful Soup rezyduje powyżej parsera HTML lub XML, zapewniając
pythonowe idiomy do iterowania, wyszukiwania i modyfikowania drzewa
analizy.

%package -n python3-%{module}
Summary:	beautifulsoup4 - Screen-scraping library
Summary(pl.UTF-8):	beautifulsoup4 - biblioteka przechwytująca wyjście
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
Beautiful Soup sits atop an HTML or XML parser, providing Pythonic
idioms for iterating, searching, and modifying the parse tree.

%description -n python3-%{module} -l pl.UTF-8
Beautiful Soup rezyduje powyżej parsera HTML lub XML, zapewniając
pythonowe idiomy do iterowania, wyszukiwania i modyfikowania drzewa
analizy.

%package apidocs
Summary:	API documentation for Python beautifulsoup4 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona beautifulsoup4
Group:		Documentation

%description apidocs
API documentation for Python beautifulsoup4 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona beautifulsoup4.

%prep
%setup -q -n beautifulsoup4-%{version}
%patch -P 0 -p1
%patch -P 2 -p1

# no longer supported by setuptools
%{__sed} -i -e '/use_2to3/d' setup.py

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m unittest discover -s bs4
%endif
%endif

%if %{with python3}
%py3_build

2to3-%{py3_ver} --no-diffs -n -w build-3/lib

%if %{with tests}
cd build-3/lib
%{__python3} -m unittest discover -s bs4
cd ../..
%endif
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/bs4/tests
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/bs4/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING.txt NEWS.txt README.md TODO.txt
%{py_sitescriptdir}/bs4
%{py_sitescriptdir}/beautifulsoup4-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc COPYING.txt NEWS.txt README.md TODO.txt
%{py3_sitescriptdir}/bs4
%{py3_sitescriptdir}/beautifulsoup4-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_images,_static,*.html,*.js}
%endif
