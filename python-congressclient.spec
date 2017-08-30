%global pypi_name congressclient

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Client for OpenStack Congress (Open Policy Framework)

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Client for OpenStack Congress (Open Policy Framework)

%package -n     python2-%{pypi_name}

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  python-cliff
BuildRequires:  python-keystoneauth1
BuildRequires:  python-mock
BuildRequires:  python-oslo-log

Requires:       python-babel >= 2.3.4
Requires:       python-cliff >= 2.8.0
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 3.22.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-pbr >= 2.0.0
Requires:       python-six >= 1.9.0

Summary:        Client for OpenStack Congress (Open Policy Framework)
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Client for OpenStack Congress (Open Policy Framework)

# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Client for OpenStack Congress (Open Policy Framework)
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-cliff
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-mock
BuildRequires:  python3-oslo-log

Requires:       python3-babel >= 2.3.4
Requires:       python3-cliff >= 2.8.0
Requires:       python3-keystoneauth1 >= 3.1.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-log >= 3.22.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-six >= 1.9.0

%description -n python3-%{pypi_name}
Client for OpenStack Congress (Open Policy Framework)
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress Client

BuildRequires: python-sphinx
BuildRequires: python-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for the client library for interacting with Openstack
Congress API.

# Documentation package
%package -n python2-%{pypi_name}-tests

Summary:  congressclient test subpackage

Requires:       python2-%{pypi_name} = %{version}-%{release}
Requires:       python-coverage >= 3.6
Requires:       python-fixtures >= 1.3.1
Requires:       python-mock
Requires:       python-testrepository >= 0.0.18
Requires:       python-testscenarios >= 0.4
Requires:       python-testtools
Requires:       python-subunit >= 0.0.18
Requires:       python-webob >= 1.2.3

%description -n python2-%{pypi_name}-tests
Test suite for OpenStack Congress (Open Policy Framework) client.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}-tests

Summary:  congressclient test subpackage

Requires:       python3-%{pypi_name} = %{version}-%{release}
Requires:       python3-coverage >= 3.6
Requires:       python3-fixtures >= 1.3.1
Requires:       python3-mock
Requires:       python3-testrepository >= 0.0.18
Requires:       python3-testscenarios >= 0.4
Requires:       python3-testtools
Requires:       python3-subunit >= 0.0.18
Requires:       python3-webob >= 1.2.3

%description -n python3-%{pypi_name}-tests
Test suite for OpenStack Congress (Open Policy Framework) client.
%endif


%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt


%build
%{__python2} setup.py build

%if 0%{?with_python3}
LANG=en_US.UTF-8 %{__python3} setup.py build
%endif

# generate html docs 
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}


%install
%if 0%{?with_python3}
LANG=en_US.UTF-8 %py3_install
%endif

%py2_install


%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info 
%exclude %{python2_sitelib}/%{pypi_name}/tests

# Files for python3
%if 0%{?with_python3}
%files -n python3-%{pypi_name} 
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests
%endif

%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%files -n python2-%{pypi_name}-tests
%{python2_sitelib}/%{pypi_name}/tests

%if 0%{?with_python3}
%files -n python3-%{pypi_name}-tests
%{python3_sitelib}/%{pypi_name}/tests
%endif


%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/python-congressclient/commit/?id=91b58c72c1c3b57a8904452aa6074e94b3526538
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/python-congressclient/commit/?id=4587128eb6009d13b8a53c5febcc2d9698871459
