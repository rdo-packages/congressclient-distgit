# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global pypi_name congressclient

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

%package -n     python%{pyver}-%{pypi_name}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr >= 2.0.0
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-cliff

Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-cliff >= 2.8.0

Summary:        Client for OpenStack Congress (Open Policy Framework)
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

# Documentation package
%package -n python%{pyver}-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress Client
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-doc}

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-sphinxcontrib-apidoc
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python%{pyver}-%{pypi_name}-doc
Documentation for the client library for interacting with Openstack
Congress API.

# Documentation package
%package -n python%{pyver}-%{pypi_name}-tests

Summary:  congressclient test subpackage

Requires:       python%{pyver}-%{pypi_name} = %{version}-%{release}
Requires:       python%{pyver}-fixtures >= 1.3.1
Requires:       python%{pyver}-mock
Requires:       python%{pyver}-testtools
Requires:       python%{pyver}-subunit >= 0.0.18
Requires:       python%{pyver}-testrepository >= 0.0.18
Requires:       python%{pyver}-testscenarios >= 0.4
Requires:       python%{pyver}-webob >= 1.2.3

%description -n python%{pyver}-%{pypi_name}-tests
Test suite for OpenStack Congress (Open Policy Framework) client.

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
%py_req_cleanup


%build
%{pyver_build}

%install
%{pyver_install}

# generate html docs
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%check
%{pyver_bin} setup.py test


%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%exclude %{pyver_sitelib}/%{pypi_name}/tests

%files -n python%{pyver}-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%files -n python%{pyver}-%{pypi_name}-tests
%{pyver_sitelib}/%{pypi_name}/tests

%changelog
