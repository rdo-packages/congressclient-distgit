%global pypi_name congressclient

%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

%if 0%{?fedora} >= 24
%global with_python3 0
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        1.2.3
Release:        2%{?dist}
Summary:        Client for OpenStack Congress (Open Policy Framework)

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Client for OpenStack Congress (Open Policy Framework)

%package -n     python2-%{pypi_name}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

Requires:       python-babel >= 1.3
Requires:       python-cliff >= 1.14
Requires:       python-keystoneclient >= 1.6.0
Requires:       python-oslo-i18n >= 1.5
Requires:       python-pbr
Requires:       python-requests >= 2.5.2
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
BuildRequires:  python3-pbr >= 0.6
BuildRequires:  python-tools

Requires:       python3-babel >= 1.3
Requires:       python3-cliff >= 1.14
Requires:       python3-keystoneclient >= 1.6.0
Requires:       python3-oslo-i18n >= 1.5
Requires:       python3-pbr
Requires:       python3-requests >= 2.5.2
Requires:       python3-six >= 1.9.0

%description -n python3-%{pypi_name}
Client for OpenStack Congress (Open Policy Framework)
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Congress Client

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx >= 2.3.0

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
Requires:       python-oslo-sphinx >= 2.5.0
Requires:       python-sphinx
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
Requires:       python3-oslo-sphinx >= 2.5.0
Requires:       python3-sphinx
Requires:       python3-subunit >= 0.0.18
Requires:       python3-webob >= 1.2.3

%description -n python3-%{pypi_name}-tests
Test suite for OpenStack Congress (Open Policy Framework) client.
%endif


%prep
%autosetup -n %{name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/%{pypi_name} %{buildroot}%{_bindir}/python3-%{pypi_name}
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# rename binaries, make compat symlinks
install -m 755 -d %{buildroot}/%{_bindir}
pushd %{buildroot}%{_bindir}
ln -s %{pypi_name} %{pypi_name}
for i in %{pypi_name}-{2,%{?python2_shortver}}; do
    ln -s %{pypi_name} $i
done
%if 0%{?with_python3}
for i in %{pypi_name}-{3,%{?python3_shortver}}; do
    ln -s  python3-%{pypi_name} $i
done
%endif
popd


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
%{_bindir}/%{pypi_name}*
%exclude %{python2_sitelib}/%{pypi_name}/tests

# Files for python3
%if 0%{?with_python3}
%files -n python3-%{pypi_name} 
%license LICENSE
%doc README.rst
%{_bindir}/python3-%{pypi_name}
%{_bindir}/%{pypi_name}*
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-%{version}-py?.?.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests
%endif

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE

%files -n python2-%{pypi_name}-tests
%{python2_sitelib}/%{pypi_name}/tests

%if 0%{?with_python3}
%files -n python3-%{pypi_name}-tests
%{python3_sitelib}/%{pypi_name}/tests
%endif


%changelog
* Wed Apr 20 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.2.3-2
- FTBFS when python3 build is enabled

* Wed Apr 20 2016 Haikel Guemar <hguemar@fedoraproject.org> 1.2.3-1
- Update to 1.2.3

* Fri Jan 22 2016 Marcos Fermin Lobo <marcos.fermin.lobo@cern.ch> 1.2.1
- First RPM
