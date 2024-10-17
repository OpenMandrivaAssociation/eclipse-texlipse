%global install_loc  %{_datadir}/eclipse/dropins/%{pkgname}
%global eclipse_base %{_libdir}/eclipse

%global pkgname      texlipse

Name:           eclipse-%{pkgname}
Version:        1.3.0
Release:        3.20090829cvs
Summary:        Eclipse plugin for editing Latex

Group:          Text tools
License:        EPL
URL:            https://texlipse.sourceforge.net

Source0:        net.sourceforge.%{pkgname}.tar.gz
# Source1 is used to download Source0
Source1:        eclipse-%{pkgname}-download.sh


# Fedora related patches as upstream default is suitable for Windows as well
#    Fedora doesn't ship acroread, hence opting for xdg-open
Patch0:         eclipse-%{pkgname}-%{version}-pdfpreview.patch
#    Remove unneccessary files
Patch1:         eclipse-%{pkgname}-bin_excludes.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  eclipse-pde
BuildRequires:  java-devel

Requires:       eclipse-platform
Requires:       tex(latex)
Requires:       xdg-utils

# For Preview
Requires:       xdvik

# For Spell-Check (choosing default : English)
Requires:       aspell-en

BuildArch:      noarch

# Ignoring rpmlint warning zero-length for Blank.tex, it is used as example

%description
Texlipse is a plugin that adds Latex editing support for the
popular Eclipse IDE.

Key features include:
    Syntax highlight, command completion, bibliography completion,
    outline navigation and automatic building.

%prep
%setup -q -c

%patch0 -p1 -b .pdfreview
%patch1 -p0 -b .exclude

find -name '*.jar' -o -name '*.class' -o -name '.cvsignore' -exec rm -f '{}' \;

# Preparing examples for %%doc
%{__cp} -pr net.sourceforge.%{pkgname}/docs/arch net.sourceforge.%{pkgname}/examples

%build

%{eclipse_base}/buildscripts/pdebuild

%install
%{__rm} -rf %{buildroot}

%{__install} -d -m 755 %{buildroot}%{install_loc}
unzip -d %{buildroot}%{install_loc} -q build/rpmBuild/net.sourceforge.%{pkgname}.zip

# Removing duplicates that should be in %%doc
%{__rm} -f %{buildroot}%{install_loc}/eclipse/plugins/net.sourceforge.%{pkgname}_%{version}/about.html

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc net.sourceforge.%{pkgname}/about.html
%doc net.sourceforge.%{pkgname}/examples
%{install_loc}


