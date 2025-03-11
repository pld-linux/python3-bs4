#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	bs4
Summary:	beautifulsoup4 - Screen-scraping library
Summary(pl.UTF-8):	beautifulsoup4 - biblioteka przechwytująca wyjście
Name:		python3-%{module}
Version:	4.13.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/beautifulsoup4/
Source0:	https://files.pythonhosted.org/packages/source/b/beautifulsoup4/beautifulsoup4-%{version}.tar.gz
# Source0-md5:	e5edd9780e91f48901f9c19ce98c5376
URL:		https://www.crummy.com/software/BeautifulSoup/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
BuildRequires:	python3-soupsieve >= 1.2
BuildRequires:	python3-typing_extensions
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	rpm-pythonprov
%if %{with doc}
BuildRequires:	sphinx-pdg-3
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

%build
%py3_build_pyproject

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest bs4/tests
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/bs4/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG LICENSE README.md
%{py3_sitescriptdir}/bs4
%{py3_sitescriptdir}/beautifulsoup4-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_images,_static,*.html,*.js}
%endif
