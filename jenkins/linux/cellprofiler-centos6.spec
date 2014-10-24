%define pkgname cellprofiler
%define pyversion 2.7
%define tarname cellprofiler
%define pref /usr/cellprofiler
%define python %{pref}/bin/python
%define githuburl git+git://github.com/CellProfiler
%define javabridge_version 1.0.9
%define bioformats_version 1.0.4
%define cython_version 0.20.2
%define numpy_version 1.9.0
%define scipy_version 0.13.2
%define pyzmq_version 2.1.11

Name:      %{pkgname}
Summary:   Cell image analysis software
Version:   %{version}
Release:   %{release}
Source0:   %{tarname}.tar.gz
License:   GPLv2
URL:       http://www.cellprofiler.org/
Packager:  Vebjorn Ljosa <ljosa@broad.mit.edu>
BuildRoot: %{_tmppath}/%{pkgname}-buildroot
Prefix:    %{pref}
Requires:  cellprofiler-cython = %{cython_version} 
Requires:  cellprofiler-python
Requires:  cellprofiler-numpy = %{numpy_version}
Requires:  cellprofiler-ilastik cellprofiler-decorator 
Requires:  cellprofiler-h5py cellprofiler-matplotlib 
Requires:  cellprofiler-mysqlpython
Requires:  cellprofiler-scipy = %{scipy_version}
Requires:  cellprofiler-scikit-learn cellprofiler-pysqlite
Requires:  cellprofiler-setuptools cellprofiler-wxpython
Requires:  cellprofiler-pyzmq = %{pyzmq_version}
Requires:  cellprofiler-jdk cellprofiler-pil
Requires:  xorg-x11-fonts-Type1 liberation-fonts-common 
Requires:  liberation-sans-fonts
Requires:  cellprofiler-javabridge = %{javabridge_version}
Requires:  cellprofiler-bioformats = %{bioformats_version}
BuildRequires: gcc gcc-c++ 
BuildRequires: cellprofiler-numpy-devel = %{numpy_version}
BuildRequires: cellprofiler-cython = %{cython_version}
BuildRequires: cellprofiler-python
BuildRequires: cellprofiler-ilastik
BuildRequires: cellprofiler-decorator
BuildRequires: cellprofiler-h5py
BuildRequires: cellprofiler-matplotlib
BuildRequires: cellprofiler-mysqlpython
BuildRequires: cellprofiler-scipy = %{scipy_version}
BuildRequires: cellprofiler-pysqlite
BuildRequires: cellprofiler-setuptools
BuildRequires: cellprofiler-wxpython
BuildRequires: cellprofiler-pyzmq = %{pyzmq_version}
BuildRequires: cellprofiler-jdk
BuildRequires: cellprofiler-javabridge

%description
Cell image analysis software

%prep

%setup -q -n CellProfiler

%build

PATH=%{pref}/bin:%{pref}/jdk/bin:$PATH \
    LD_LIBRARY_PATH=%{pref}/jdk/lib:%{pref}/jdk/jre/lib/amd64/server: \
    JAVA_HOME=%{pref}/jdk \
    MAVEN_OPTS="-Xmx1024m" \
    python external_dependencies.py

PATH=%{pref}/bin:%{pref}/jdk/bin:$PATH \
    LD_LIBRARY_PATH=%{pref}/jdk/lib:%{pref}/jdk/jre/lib/amd64/server: \
    JAVA_HOME=%{pref}/jdk \
    python CellProfiler.py --build-and-exit --do-not-fetch

patch <<EOF
--- CellProfiler.py.orig	2013-10-16 20:59:07.459360385 -0400
+++ CellProfiler.py	2013-10-16 20:16:34.079360393 -0400
@@ -20,6 +20,8 @@
 import tempfile
 from cStringIO import StringIO
 
+sys.frozen = True
+
 if sys.platform.startswith('win'):
     # This recipe is largely from zmq which seems to need this magic
     # in order to import in frozen mode - a topic the developers never
EOF

%install

mkdir -p $RPM_BUILD_ROOT%{pref}/src
cp -a . $RPM_BUILD_ROOT%{pref}/src/CellProfiler

PATH=%{pref}/bin:%{pref}/jdk/bin:$PATH \
    LD_LIBRARY_PATH=%{pref}/jdk/lib:%{pref}/jdk/jre/lib/amd64/server: \
    JAVA_HOME=%{pref}/jdk \
%{python} cellprofiler/utilities/setup.py install --root=$RPM_BUILD_ROOT

PATH=%{pref}/bin:%{pref}/jdk/bin:$PATH \
    LD_LIBRARY_PATH=%{pref}/jdk/lib:%{pref}/jdk/jre/lib/amd64/server: \
    JAVA_HOME=%{pref}/jdk \
%{python} cellprofiler/cpmath/setup.py install --root=$RPM_BUILD_ROOT

#echo "version_string = '`date +%%Y-%%m-%%dT%%H:%%M:%%S` %{version}'" > $RPM_BUILD_ROOT%{pref}/src/CellProfiler/cellprofiler/frozen_version.py
(cd $RPM_BUILD_ROOT%{pref}/src/CellProfiler; PYTHONPATH=. ./jenkins/linux/make_frozen_version.py)

mkdir $RPM_BUILD_ROOT/usr/bin
cp usr-bin-cellprofiler $RPM_BUILD_ROOT/usr/bin/cellprofiler
chmod 755 $RPM_BUILD_ROOT/usr/bin/cellprofiler

%clean

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{pref}/src/CellProfiler
%{pref}/lib/python%{pyversion}/site-packages/_convex_hull.so
%{pref}/lib/python%{pyversion}/site-packages/_cpmorphology.so
%{pref}/lib/python%{pyversion}/site-packages/_cpmorphology2.so
%{pref}/lib/python%{pyversion}/site-packages/_filter.so
%{pref}/lib/python%{pyversion}/site-packages/_fastemd.so
%{pref}/lib/python%{pyversion}/site-packages/_lapjv.so
%{pref}/lib/python%{pyversion}/site-packages/_propagate.so
%{pref}/lib/python%{pyversion}/site-packages/_watershed.so
%{pref}/lib/python%{pyversion}/site-packages/cpmath-0.0.0-py2.7.egg-info
%{pref}/lib/python%{pyversion}/site-packages/utilities-0.0.0-py2.7.egg-info
/usr/bin/cellprofiler
