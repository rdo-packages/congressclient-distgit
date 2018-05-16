%global pypi_name congressclient

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Client for OpenStack Congress (Open Policy Framework)

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Client for OpenStack Congress (Open Policy Framework)

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python2-%{pypi_name}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr >= 2.0.0
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-mock
BuildRequires:  python2-oslo-log
%if 0%{?fedora} > 0
BuildRequires:  python2-cliff
%else
BuildRequires:  python-cliff
%endif

Requires:       python2-babel >= 2.3.4
Requires:       python2-keystoneauth1 >= 3.3.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-pbr >= 2.0.0
Requires:       python2-six >= 1.10.0
%if 0%{?fedora} > 0
Requires:       python2-cliff >= 2.8.0
%else
Requires:       python-cliff >= 2.8.0
%endif

Summary:        Client for OpenStack Congress (Open Policy Framework)
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{common_desc}

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
Requires:       python3-keystoneauth1 >= 3.3.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-six >= 1.10.0

%description -n python3-%{pypi_name}
%{common_desc}
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress Client

BuildRequires: python-sphinx
BuildRequires: python-sphinxcontrib-apidoc
BuildRequires: python-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for the client library for interacting with Openstack
Congress API.

# Documentation package
%package -n python2-%{pypi_name}-tests

Summary:  congressclient test subpackage

Requires:       python2-%{pypi_name} = %{version}-%{release}
Requires:       python2-fixtures >= 1.3.1
Requires:       python2-mock
Requires:       python2-testtools
Requires:       python2-subunit >= 0.0.18
%if 0%{?fedora} > 0
Requires:       python2-testrepository >= 0.0.18
Requires:       python2-testscenarios >= 0.4
Requires:       python2-webob >= 1.2.3
%else
Requires:       python-testrepository >= 0.0.18
Requires:       python-testscenarios >= 0.4
Requires:       python-webob >= 1.2.3
%endif

%description -n python2-%{pypi_name}-tests
Test suite for OpenStack Congress (Open Policy Framework) client.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}-tests

Summary:  congressclient test subpackage

Requires:       python3-%{pypi_name} = %{version}-%{release}
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
%py_req_cleanup


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

# generate html docs
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

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
