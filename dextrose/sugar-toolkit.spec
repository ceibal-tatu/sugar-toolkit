%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

# Environment setup:
#
#	mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
#	echo | bzip2 -c > ~/rpmbuild/SOURCES/sugar-toolkit.tar.bz2
#	cd ~/build/ && git clone git://git.sugarlabs.org/dextrose/sugar.git
#	ln -s ~/build/sugar/dextrose/sugar-toolkit.spec \
#	      ~/rpmbuild/SPECS/sugar-tookit-gtk3.spec
#	rpmbuild -ba ~/rpmbuild/SPECS/sugar-toolkit.spec
#

%define git_repo sugar-toolkit
%define git_head devel

%define git_repodir %(echo ~/build/)
%define git_gitdir %{git_repodir}/%{git_repo}/.git

%define git_get_source pushd %{git_repodir}/%{git_repo} ;\
#	/usr/bin/git pull ;\
        /usr/bin/git archive --format=tar --prefix=%{name}-%{version}/ %{git_head} | \
                bzip2 -c > %{_sourcedir}/%{name}-%{version}.tar.bz2 ;\
        popd

%define git_clone_source if [ -d %{name}-%{version} ] ; then \
                cd %{name}-%{version} && git pull origin %{git_head} ; \
        else \
                git clone %{git_gitdir} %{name}-%{version} && \
                cd %{name}-%{version}/ ; \
        fi

%define git_submodule git submodule
%define git_prep_submodules %{git_submodule} init --cloned && %{git_submodule} update

%define git_version %(git --git-dir=%{git_gitdir} describe --tags 2> /dev/null || echo 0.0-`git --git-dir=%{git_gitdir} log --oneline | wc -l`-g`git --git-dir=%{git_gitdir} describe --always`)

# if the git repo has tags
%define git_get_ver %(echo %{git_version} | sed 's/^v\\?\\(.*\\)-\\([0-9]\\+\\)-g.*$/\\1/;s/-//')
%define git_get_rel %(echo %{git_version} | sed 's/^v\\?\\(.*\\)-\\([0-9]\\+-g.*\\)$/\\2/;s/-/_/')



Summary: Sugar toolkit
Name: sugar-toolkit
Epoch: 1
Version: %git_get_ver
Release: %git_get_rel
URL: http://wiki.laptop.org/go/Sugar
Source0: http://download.sugarlabs.org/sources/sucrose/glucose/%{name}/%{name}-%{version}.tar.bz2
Source1: macros.sugar
License: LGPLv2+
Group: System Environment/Libraries

BuildRequires: alsa-lib-devel
BuildRequires: gettext-devel
BuildRequires: gtk2-devel
BuildRequires: intltool
BuildRequires: libSM-devel
BuildRequires: perl-XML-Parser
BuildRequires: pkgconfig
BuildRequires: pygtk2-devel

Requires: dbus-python
Requires: gettext
Requires: gnome-python2-gconf
Requires: gnome-python2-rsvg
Requires: hippo-canvas-python
Requires: pygtk2
Requires: python-simplejson
Requires: python-dateutil
Requires: sugar-base
Requires: sugar-datastore
Requires: sugar-presence-service
Requires: unzip

%description
Sugar is the core of the OLPC Human Interface. The toolkit provides
a set of widgets to build HIG compliant applications and interfaces
to interact with system services like presence and the datastore.

%prep
%git_get_source
%setup -q

%build
sh autogen.sh
autoreconf -i
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/rpm/
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.sugar

%find_lang %name

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README
%{python_sitelib}/*
%{_sysconfdir}/rpm/macros.sugar

%changelog
* Thu Jan 31 2013 Santiago Rodriguez <scollazo@activitycentral.com>  0.98.0-dx2
- Sugar 0.98 stable release

* Thu Nov 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.98.0-1
- Sugar 0.98 stable release

* Tue Nov 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.97.2-1
- 0.97.2 devel release

* Sat Oct  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.97.1-2
- Add gnome-python2-gconf dependency

* Fri Oct  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.97.1-1
- 0.97.1 devel release

* Tue Aug 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.97.0-1
- 0.97.0 devel release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.3-1
- 0.96.3 stable release

* Sat Jun  2 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.2-1
- 0.96.2 stable release

* Sun May 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.1-2
- Add gettext to Requires

* Sat May  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.1-1
- 0.96.1 stable release

* Tue Apr 24 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.96.0-1
- 0.96.0 stable release

* Wed Mar  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.95.4-1
- devel release 0.95.4

* Fri Mar  2 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.95.3-1
- devel release 0.95.3

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.95.2-1
- devel release 0.95.2

* Tue Oct 25 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.95.1-1
- devel release 0.95.1

* Thu Sep 29 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.94.0-1
- 0.94.0 stable release

* Tue Sep 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.93.4-1
- 0.93.4 dev release

* Wed Sep  7 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.93.3-1
- 0.93.3 dev release

* Fri Aug 19 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.93.2-1
- 0.93.2 dev release

* Mon Jul 25 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.92.4-1
- 0.92.4

* Thu Jun  9 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.92.2-1
- 0.92.2 release

* Thu Apr 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.92.1-1
- 0.92.1 release

* Mon Feb 28 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.92.0-1
- 0.92.0 release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.90.2-3
- Drop fonts patch as its causing issues

* Sat Jan 29 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.90.2-2
- bump build

* Fri Oct 15 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.90.2-1
- 0.90.2 release

* Tue Oct  5 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.90.1-1
- 0.90.1 release

* Wed Sep 29 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.90.0-1
- 0.90.0 stable release

* Mon Aug 30 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.89.5-1
- New upstream devel 0.89.5 release

* Wed Aug 25 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.89.4-1
- New upstream devel 0.89.4 release

* Tue Aug 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.89.3-1
- New upstream devel 0.89.3 release

* Tue Aug 17 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.89.2-1
- New upstream devel 0.89.2 release

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.89.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 14 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.89.1-1
- New upstream devel 0.89.1 release

* Thu Jun  3 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.88.1-1
- New upstream stable 0.88.1 release

* Tue Mar 20 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.88.0-1
- New upstream stable 0.88.0 release

* Wed Mar 10 2010 Sebastian Dziallas <sebastian@when.com> - 0.87.8-1
- New upstream release

* Wed Feb 17 2010 Sebastian Dziallas <sebastian@when.com> - 0.87.6-1
- New upstream release

* Tue Feb 16 2010 Sebastian Dziallas <sebastian@when.com> - 0.87.5-4
- Make sure to use correct patch

* Tue Feb 16 2010 Sebastian Dziallas <sebastian@when.com> - 0.87.5-3
- Enable sugar-settings-manager support

* Sat Feb 13 2010 Simon Schampijer <simon@schampijer.de> - 0.87.5-2
- Add the requires field for python-dateutil (brings back activity start)

* Thu Feb 11 2010 Sebastian Dziallas <sebastian@when.com> - 0.87.5-1
- New upstream release

* Sun Feb 07 2010 Sebastian Dziallas <sebastian@when.com> - 0.87.4-1
- New upstream release

* Tue Jan 12 2010 Sebastian Dziallas <sebastian@when.com> - 0.87.3-1
- New upstream release

* Sat Jan  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.87.2-2
- Updated to the new python sysarch spec file reqs

* Wed Dec 23 2009 Sebastian Dziallas <sebastian@when.com> - 0.87.2-1
- New upstream release

* Fri Dec 18 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.87.1-2
- Remove libtool archives

* Tue Dec 01 2009 Sebastian Dziallas <sebastian@when.com> - 0.87.1-1
- New upstream release

* Wed Oct 21 2009 Sebastian Dziallas <sebastian@when.com> - 0.86.2-1
- Do not stop processing motion-notify-event #1507

* Tue Oct 13 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 0.86.0-3
- Add unzip as a dependency

* Fri Oct 09 2009 Luke Macken <lmacken@redhat.com> - 0.86.0-2
- Remove python-json requirement, which is now provided by Python 2.6

* Sun Sep 27 2009 Sebastian Dziallas <sebastian@when.com> - 0.86.0-1
- New upstream release

* Fri Sep 18 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 0.85.8-1
- New upstream release

* Fri Sep 11 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 0.85.7-1
- New upstream release

* Wed Sep 05 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 0.85.6-2
- Drop Requires: gettext, it should be just a BuildReq

* Wed Sep 02 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 0.85.6-1
- New upstream release

* Wed Aug 26 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 0.85.5-1
- New upstream release

* Sun Aug 02 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 0.85.3-1
- New upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 0.85.2-1
- New upstream release

* Mon Apr 06 2009 Simon Schampijer <simon@schampijer.de> - 0.84.4-1
- new german and spanish translations

* Mon Apr 06 2009 Simon Schampijer <simon@schampijer.de> - 0.84.3-1
- Journal Palette does not manage too many characters for a title correctly #610
- Bundlebuilder list_files: Better error handling #635
- Only call read_file once on activity startup #428
- Revert "Listen for map in Window instead of in Canvas (alsroot) #428"
- Use git ls-files instead of git-ls-files, to work with newer Git. d.sl.o #647
- Bundlebuilder: Don't include whole directory in src tarball #397

* Wed Apr 01 2009 Simon Schampijer <simon@schampijer.de> - 0.84.1-2.20090401git0a65259dc5
- git snapshot

* Sun Mar 22 2009 Simon Schampijer <simon@schampijer.de> - 0.84.1-1
- Fix palettes scaling when using scaling factor 72 #504
- Use Popen.communicate() to avoid hang (Sascha Silbe) #397
- Change property type to object because int cannot be None #157

* Wed Mar 18 2009 Simon Schampijer <simon@schampijer.de> - 0.84.0-2.20090318git29aa6cbe65
- git snapshot

* Tue Mar 03 2009 Simon Schampijer <simon@schampijer.de> - 0.84.0-1
- Catch all exceptions while saving #224
- Listen for map in Window instead of in Canvas (alsroot) #428
- Restore minimal .xol support #459
- Use the same font size independent from scaling
- Don't recursively clean an activity if it's a symbolic link #444
- Add extension to temp icon file names #458
- Process .py files in subdirectories './setup genplot' #391 (alsroot)
- Improve error handling of calls to XGrabKey #431
- Cleanup temp files at exit #435
- Let activities provide their own implementation of get_preview() #152
- Show/Hide the color palette correctly (#374)
- Support setting None as the secondary text #384
- Only display one line in the secondary text of a clipping palette #384
- Switch to existing instance of an activity if it's already running #410
- Reveal the palette on right click on an activity icon #409

* Fri Feb 27 2009 Simon Schampijer <simon@schampijer.de> - 0.83.7-3.20090227git6f210f0e33
- git snapshot
- Process .py files in subdirectories './setup genplot' #391 (alsroot)
- Improve error handling of calls to XGrabKey #431
- Cleanup temp files at exit #435
- Let activities provide their own implementation of get_preview() #152
- Show/Hide the color palette correctly (#374)
- Support setting None as the secondary text #384
- Only display one line in the secondary text of a clipping palette #384
- Switch to existing instance of an activity if it's already running #410
- Reveal the palette on right click on an activity icon #409

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Simon Schampijer <simon@schampijer.de> - 0.83.7-1
- Don't try to hide the tray if the activity has none (alsroot) #395
- NamingAlert: Icon dependent on the entry type #353
- Updated Languages

* Mon Feb 16 2009 Simon Schampijer <simon@schampijer.de> - 0.83.6-1
- Dates in journal are not translated #55
- Keep error when displaying a file in Browse, Read, ImageViewer, etc #258
- Palette positioning fixes #298
- 'Resume' activity window when NamingAlert is displayed #293
- Naming alert prevents activity close on keep error #224

* Fri Feb 06 2009 Simon Schampijer <simon@schampijer.de> - 0.83.5-2.20090206git474b2c3476
- Set the locale path for sugar-toolkit #55
- Don't push to the DS a file path pointing to nowhere #258

* Wed Feb 04 2009 Simon Schampijer <simon@schampijer.de> - 0.83.5-1
- Palette positioning fixes #298
- 'Resume' activity window when NamingAlert is displayed #293
- Naming alert prevents activity close on keep error #224

* Fri Jan 30 2009 Simon Schampijer <simon@schampijer.de> - 0.83.4-2.20090130git073336585d
- Translation updates
- Naming alert prevents activity close on keep error #224

* Tue Jan 20 2009 Marco Pesenti Gritti <mpg@redhat.com> - 0.83.4-1
- separate debug settings from xsession #163
- show an alert on activity close for suggesting the user to set properties of the entry #215
- add a colorpicker to Sugar, only the ColorToolButton is public for now
- move the palette to new style gobject properties
- #3060 Add the possibility of filtering the object chooser by data type
- fix uninstallling of activities that use symlinks #171
- remove the hacks for asking the X server for screenshots and use gtk.Widget.get_snapshot() instead

* Sun Jan 04 2009 Simon Schampijer <simon@laptop.org> - 0.83.3-1
- remove session shutdown patch
- add intltool as build requires
- new download url
- Fix palette highlighting on tray icons. Patch by benzea, style tweaks by marcopg
- Rework palette state logic. Fix #42
- Use g_timeout_add_seconds() for power efficiency
- Add colors to icons in menu items
- Add accelerator support to menu items
- Simplify activity bundle installation
- Dont pop down the palette when a submenu opens

* Mon Dec  5 2008 Peter Robinson<pbrobinson@fedoraproject.org> - 0.83.2-4
- Rebuild for python 2.6

* Sat Nov 29 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.83.2-3
- Fix session shutdown

* Fri Nov 28 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.83.2-1
- Update to 0.83.2

* Tue Nov  4 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.83.1-2
- Update to 0.83.1

* Wed Sep 24 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.82.11-1
- #8626 Icons overlap unnecessarily in crowded neighborhood view.

* Sat Sep 20 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.82.10-1
- #8532 SIGCHLD fights with threads.
- #8485 Switching between zoom levels seem to leak

* Tue Sep 16 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.82.8-2
- Fix a crash when we cannot access the alsa device

* Sat Sep 13 2008 Simon Schampijer <simon@laptop.org> - 0.82.7-1
- #8375 gst usage in the shell wastes 2.6mb
- #8394 sugar shell leaks presence service info
- #8469 palette.menu is leaked

* Thu Sep 11 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.82.6-1
- #8394 sugar shell leaks presence service info
- #8392 Remove "dynamic" font height computation

* Tue Sep 9 2008 Simon Schampijer <simon@laptop.org> - 0.82.5-4
- remove pseudo.po from the source tarball

* Wed Sep  3 2008 Jeremy Katz <katzj@redhat.com> - 0.82.5-3
- requires gettext for bundlebuilder

* Mon Sep 01 2008 Simon Schampijer <simon@laptop.org> - 0.82.5-2
- added the python-json dependency

* Mon Sep 01 2008 Simon Schampijer <simon@laptop.org> - 0.82.5-1
- Translation updates
- Add plural information for all languages
- Fix plural form equations

* Thu Aug 31 2008 Simon Schampijer <simon@laptop.org> - 0.82.4-1
- 8136 Do a more 'standard' system installation for bundlebuilder
- 7837 Do not try to list the mimetypes directory if it does not exist
- 8220 Ensure that the widget is fully onscreen before taking a screenshot

* Thu Aug 28 2008 Marco Pesenti Gritti <mpgritti@gmail.com> - 0.82.3-1
- Translation updates

* Thu Aug 28 2008 Marco Pesenti Gritti <mpgritti@gmail.com> - 0.82.2-1
- #5428 downloads not starting in Browse due to old compreg.dat
- #7733 Cannot install Wikipedia-10.xo
- #7533 Activity does not respond to ctrl-q keyboard shortcut unless the 'Activity' tab is visible
- #8000 Pulsing icon on activity launch significantly slows activity start-up
- #8000 Pulsing icon on activity launch significantly slows activity start-up
- #7270 /setup release does not update the bundle number
- #7680 Activity name box is too small for localizaed name
- #7881 Accelerator labels don't show up for most toolbar buttons
- #7800 time stamps doesn't use translations

* Tue Aug 22 2008 Tomeu Vizoso <tomeu@tomeuvizoso.net> - 0.82.1-2.20080822git2e6be9ea55
- #7270 Add update functionality to Config in bundlebuilder
- #7680 Widen activity tile entry
- #7841 Wrap message in alert
- #7881 Make Palette handle changes of the invoker widget

* Tue Aug 12 2008 Marco Pesenti Gritti <mpgritti@gmail.com> - 0.82.1-1
- Fix crash on startup on x86_64

* Thu Aug 07 2008 Marco Pesenti Gritti <mpgritti@gmail.com> - 0.82.0-2
- Rebuild

* Thu Aug 07 2008 Marco Pesenti Gritti <mpgritti@gmail.com> - 0.82.0-1
- #7759 Default home view should be Ring, not Freeform
- #4084 Palette persist over zoom levels
- #7754 Handle multiple Activity per process correctly
- Add git tagging to the 'setup.py release' command

* Fri Aug 01 2008 Morgan Collett <morgan@laptop.org> - 0.81.8-1
- #7566 sugar-shell enters in infinite loop after a failed shutdown
- #7534 Safer to always install, rather than comparing versions
- #7494 Updates to Browse-92 fail

* Wed Jul 23 2008 Simon Schampijer <simon@laptop.org> - 0.81.7-1
- 5136 Keep error alert hard to find
- 6014 Shutdown should sync activities data
- 7532 install + open content bundles with journal
- 7523 library index regeneration fails due to no XDG_DATA_DIRS
- 4208 Battery indicator's icon fullness inconsistent with indicator %.
- 7444 cannot close a shared activity when the initiator has disconnected
- 7430 Favorites view is not preserved
- 7434 Control panel UI for power management.
- 5079 Could simplify sharing code

* Tue Jul 15 2008 Simon Schampijer <simon@laptop.org> - 0.81.6-3.20080715gitd17347cc19
- git snapshot
- 7523 fix content bundle installation
- 5079 simplify sharing code
- 4208 get_icon_state accepts negative step kwarg
- 7444 Fix crash in get_joined_buddies when a buddy disappears uncleanly

* Wed Jul 09 2008 Simon Schampijer <simon@laptop.org> - 0.81.6-2.20080709git92ef9d298a
- git snapshot
- 7430 Preserve the favorites layout across reboots
- 7434 Add power section to the control panel

* Wed Jul 09 2008 Simon Schampijer <simon@laptop.org> - 0.81.6-1
- 7015 Add proper alignment support to the tray control
- 7054 Journal doesn't show correct colors for activity instances
- 7046 Deleting activity bundle with journal leaves it showing in Home list view until reboot
- 3939 Keep button should use XO colors
- 7248 Speaker device has inconsistent behavior

* Sat Jun 21 2008 Tomeu Vizoso <tomeu@tomeuvizoso.net> - 0.81.5-1
- Add build dependency on libSM-devel
- Support for session management (marco)
- Make MANIFEST mandatory in bundlebuilder (homunq)
- Add a position attribute to activity bundles (tomeu)
- Add a scroll_to_item method to the tray (benzea)

* Mon Jun 09 2008 Simon Schampijer <simon@laptop.org> - 0.81.4-1
- Add an installation time property to the activity bundle (Tomeu)
- Reveal palettes on right-click (Eben)
- Refactor bundlebuilder and add dist_source command (Marco)
- Enable journal to do open-with for activity bundles (Chema)
- Add timezone, hot_corners, warm_edges to the profile (Simon)

* Thu Apr 24 2008 Simon Schampijer <simon@laptop.org> - 0.79.6-1
- Fix activity installation

* Tue Apr 22 2008 Tomeu Vizoso <tomeu@tomeuvizoso.net> - 0.79.5-1
- Correctly use tempfile.mkstemp().

* Tue Apr 22 2008 Tomeu Vizoso <tomeu@tomeuvizoso.net> - 0.79.4-1
- Pylint cleanup.

* Wed Apr 09 2008 Tomeu Vizoso <tomeu@tomeuvizoso.net> - 0.79.3
- Added default to label arg in palette constructor (eben)

* Fri Apr 04 2008 Dennis Gilmore <dennis@ausil.us> - 0.79.2-3
- add macro defining sugaractivitydir

* Thu Apr 03 2008 Simon Schampijer <simon@laptop.org> - 0.79.2
- add python-simplejson as dependency
- #5474: Scale emblems

* Wed Apr  2 2008 Simon Schampijer <simon@laptop.org> - 0.79.1
- Frame/Home redesign - Put corner stone

* Fri Feb  8 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.79.0-2
- Fix source reference

* Wed Feb  6 2008 Marco Pesenti Gritti <mpg@redhat.com> - 0.79.0-1
- Initial build
