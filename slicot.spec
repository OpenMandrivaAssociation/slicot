# For now -- since C code (built with clang) and
# Fortran code (built with gfortran) are linked
# together, LTO object files don't work
%global _disable_lto 1

# BLAS lib
%global blaslib flexiblas

%define major 0
%define libname %mklibname slicot
%define devname %mklibname slicot -d

Summary:	Subroutine Library in Systems and Control Theory 
Name:		slicot
Version:	5.9
Release:	1
License:	BSD-3-Clause
Group:		System/Libraries
URL:		https://www.slicot.org/
#Source0:	https://github.com/SLICOT/SLICOT-Reference/archive/%{?snapshot:master}%{!?snapshot:v%{version}}/%{name}-%{?snapshot:master}%{!?snapshot:%{version}}.tar.gz
Source0:	https://github.com/SLICOT/SLICOT-Reference/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	gcc-gfortran
BuildRequires:	pkgconfig(%{blaslib})

%description
The subroutine library SLICOT provides Fortran 77 implementations
of numerical algorithms for computations in systems and control
theory.  Based on numerical linear algebra routines from BLAS and
LAPACK libraries, SLICOT provides methods for the design and
analysis of control systems.

The basic ideas behind the library are:

 1. usefulness of algorithms;
 2. robustness, algorithms must either return reliable results or
    an error or warning indicator;
 3. numerical stability and accuracy: the results are as good as
    can be expected when working at a given precision. If possible
    an estimate of the achieved accuracy should be given;
 4. performance with respect to speed and memory requirements. Although
    important because of ever increasing complexity of control problems,
    this objective may never be met at cost of the two previous ones;
 5. portability and reusability: the library should be independent of
    platforms;
 6. standardisation: the library is based on rigorous programming and
    documentation standards;
 7. benchmarking, i.e., a standardised set of examples that allows an
    evaluation of the performance of a method as well as the implementation
    with respect to correctness, accuracy, and speed. Benchmarking gives
    also insight in the behaviour of the method and its implementation in
    extreme situations, i.e., for problems where the limit of the possible
    accuracy is reached.

#-----------------------------------------------------------------------

%package -n %{libname}
Summary:	Subroutine Library in Systems and Control Theory 
Group: System/Libraries

%description -n %{libname}
The subroutine library SLICOT provides Fortran 77 implementations
of numerical algorithms for computations in systems and control
theory.  Based on numerical linear algebra routines from BLAS and
LAPACK libraries, SLICOT provides methods for the design and
analysis of control systems.

The basic ideas behind the library are:

 1. usefulness of algorithms;
 2. robustness, algorithms must either return reliable results or
    an error or warning indicator;
 3. numerical stability and accuracy: the results are as good as
    can be expected when working at a given precision. If possible
    an estimate of the achieved accuracy should be given;
 4. performance with respect to speed and memory requirements. Although
    important because of ever increasing complexity of control problems,
    this objective may never be met at cost of the two previous ones;
 5. portability and reusability: the library should be independent of
    platforms;
 6. standardisation: the library is based on rigorous programming and
    documentation standards;
 7. benchmarking, i.e., a standardised set of examples that allows an
    evaluation of the performance of a method as well as the implementation
    with respect to correctness, accuracy, and speed. Benchmarking gives
    also insight in the behaviour of the method and its implementation in
    extreme situations, i.e., for problems where the limit of the possible
    accuracy is reached.

%files -n %{libname}
%license LICENSE
%{_libdir}/lib%{name}*.so.%{major}*

#-----------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%files -n %{devname}
%license LICENSE
%doc README.md ReleaseNotes.md
%doc libindex.html doc/
%doc examples/
%{_libdir}/lib%{name}*.so

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n SLICOT-Reference-%{?snapshot:main}%{?!snapshot:%{version}}

#sed -Ei "s/^OPTS = .*/OPTS = %{optflags} -ffat-lto-objects/" make_Unix.inc

%build
export FC=gfortran

export SOVER=0
#configure
%setup_compile_flags
export FFLAGS="$FFLAGS -fPIC -fdefault-integer-8"

#make_build -f makefile_Unix lib FC="$FC" FFLAGS="$FFLAGS" SLICOTLIB="../libslicot.a"
#make_build -f makefile_Unix lib FC="$FC" FFLAGS="$FFLAGS" SLICOTLIB="../libslicot_pic.a"
#$FC $LDFLAGS -shared -Wl,-soname=libslicot.so.%{major} -o libslicot.so.%{major} -Wl,--whole-archive libslicot_pic.a -Wl,--no-whole-archive -l%{blaslib}
#%make_build -f makefile_Unix lib FORTRAN="$(FC)" OPTS="$(FFLAGS) -fPIC -fdefault-integer-8" SLICOTLIB="../libslicot64_pic.a"

%make_build -f makefile_Unix \
	lib FORTRAN="$FC" OPTS="$FFLAGS -fPIC" ARCH="gcc-ar" \
	SLICOTLIB="../libslicot_pic.a"

${FC} ${LDFLAGS} -shared -Wl,-soname=libslicot.so.${SOVER} -o libslicot.so.${SOVER} -Wl,--whole-archive libslicot_pic.a -Wl,--no-whole-archive -l%{blaslib}64
ln -snf libslicot.so.${SOVER} libslicot.so

%install
#make_install -f makefile_Unix

# lib
install -pm 0755 -d %{buildroot}%{_libdir}/
install -pm 0755 libslicot.so.%{major}* %{buildroot}%{_libdir}/
#install -pm 0755 libslicot.so %{buildroot}%{_libdir}/
ln -fns libslicot.so.%{major} %{buildroot}%{_libdir}/libslicot.so

