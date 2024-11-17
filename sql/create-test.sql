-- password for both users is 'abcde'
INSERT INTO users (username, chosen_name, password, active, source, comment) VALUES (
    'user_1', 'Teacher', '$argon2id$v=19$m=65536,t=3,p=4$DY/5l6SA/SO+dZ6Q0Yb5Hg$LSZuOeEuoCy+H7OOH2oVBE6/ssA7NtPZ9Nxup1aT5jU', true, 0, 'Created in SQL'
);

INSERT INTO users (username, chosen_name, password, active, source, comment) VALUES (
    'user_2', 'Student', '$argon2id$v=19$m=65536,t=3,p=4$DY/5l6SA/SO+dZ6Q0Yb5Hg$LSZuOeEuoCy+H7OOH2oVBE6/ssA7NtPZ9Nxup1aT5jU', true, 0, 'Created in SQL'
);


INSERT INTO userRoles (user_id, role_id) VALUES (
    1, 1
);

INSERT INTO userRoles (user_id, role_id) VALUES (
    2, 2
);

INSERT INTO courses (codename, title, description, mode, created, modified) VALUES (
    'MAA05',
    'Pitkä matematiikka: Funktiot ja trigonometria 2',
    'Lorem ipsum dolor sit amet..',
    0,
    170000000,
    170000000
);

INSERT INTO courses (codename, title, description, mode, created, modified) VALUES (
    'MAA06',
    'Pitkä matematiikka: Derivaatta',
    'Lorem ipsum dolor sit amet..',
    1,
    170000000,
    170000000
);

-- Course codes/'passwords' are not hashed because theyre not meant to be a serious security measure
INSERT INTO courses (codename, title, description, mode, code, created, modified) VALUES (
    'FY8',
    'Aine, säteily ja kvantittuminen',
    'Lorem ipsum dolor sit amet..',
    2,
    'salasana',
    170000000,
    170000000
);


INSERT INTO courseMembers (user_id, course_id, user_type) VALUES (
    1, 2, 0
);


INSERT INTO courseMaterials (course_id, material_type, content, name) VALUES (
    2,
    0,
    'Hello World!',
    'Lyhyt testi'
);

INSERT INTO courseMaterials (course_id, material_type, content, name) VALUES (
    2,
    1,
    'Hello World!',
    'Lyhyt testi'
);

-- from wikipedia
INSERT INTO courseMaterials (course_id, material_type, content, name) VALUES (
    2,
    2,
    '<p>Python was invented in the late 1980s<sup id="cite_ref-venners-interview-pt-1_41-0" class="reference"><a href="#cite_note-venners-interview-pt-1-41"><span class="cite-bracket">&#91;</span>41<span class="cite-bracket">&#93;</span></a></sup> by <a href="/wiki/Guido_van_Rossum" title="Guido van Rossum">Guido van Rossum</a> at <a href="/wiki/Centrum_Wiskunde_%26_Informatica" title="Centrum Wiskunde &amp; Informatica">Centrum Wiskunde &amp; Informatica</a> (CWI) in the <a href="/wiki/Netherlands" title="Netherlands">Netherlands</a> as a successor to the <a href="/wiki/ABC_programming_language" class="mw-redirect" title="ABC programming language">ABC programming language</a>, which was inspired by <a href="/wiki/SETL" title="SETL">SETL</a>,<sup id="cite_ref-AutoNT-12_42-0" class="reference"><a href="#cite_note-AutoNT-12-42"><span class="cite-bracket">&#91;</span>42<span class="cite-bracket">&#93;</span></a></sup> capable of <a href="/wiki/Exception_handling" title="Exception handling">exception handling</a> and interfacing with the <a href="/wiki/Amoeba_(operating_system)" title="Amoeba (operating system)">Amoeba</a> operating system.<sup id="cite_ref-faq-created_12-1" class="reference"><a href="#cite_note-faq-created-12"><span class="cite-bracket">&#91;</span>12<span class="cite-bracket">&#93;</span></a></sup> Its implementation began in December&#160;1989.<sup id="cite_ref-timeline-of-python_43-0" class="reference"><a href="#cite_note-timeline-of-python-43"><span class="cite-bracket">&#91;</span>43<span class="cite-bracket">&#93;</span></a></sup> Van Rossum shouldered sole responsibility for the project, as the lead developer, until 12 July 2018, when he announced his "permanent vacation" from his responsibilities as Pythons "<a href="/wiki/Benevolent_dictator_for_life" title="Benevolent dictator for life">benevolent dictator for life</a>" (BDFL), a title the Python community bestowed upon him to reflect his long-term commitment as the projects chief decision-maker<sup id="cite_ref-lj-bdfl-resignation_44-0" class="reference"><a href="#cite_note-lj-bdfl-resignation-44"><span class="cite-bracket">&#91;</span>44<span class="cite-bracket">&#93;</span></a></sup> (he has since come out of retirement and is self-titled "BDFL-emeritus"). In January&#160;2019, active Python core developers elected a five-member Steering Council to lead the project.<sup id="cite_ref-45" class="reference"><a href="#cite_note-45"><span class="cite-bracket">&#91;</span>45<span class="cite-bracket">&#93;</span></a></sup><sup id="cite_ref-46" class="reference"><a href="#cite_note-46"><span class="cite-bracket">&#91;</span>46<span class="cite-bracket">&#93;</span></a></sup></p><p>Python 2.0 was released on 16 October 2000, with many major new features such as <a href="/wiki/List_comprehension" title="List comprehension">list comprehensions</a>, <a href="/wiki/Cycle_detection" title="Cycle detection">cycle-detecting</a> garbage collection, <a href="/wiki/Reference_counting" title="Reference counting">reference counting</a>, and <a href="/wiki/Unicode" title="Unicode">Unicode</a> support.<sup id="cite_ref-newin-2.0_47-0" class="reference"><a href="#cite_note-newin-2.0-47"><span class="cite-bracket">&#91;</span>47<span class="cite-bracket">&#93;</span></a></sup> Python&#160;3.0 was released on 3 December 2008, with many of its major features <a href="/wiki/Backporting" title="Backporting">backported</a> to Python&#160;2.6.x<sup id="cite_ref-pep-3000_48-0" class="reference"><a href="#cite_note-pep-3000-48"><span class="cite-bracket">&#91;</span>48<span class="cite-bracket">&#93;</span></a></sup> and 2.7.x. Releases of Python&#160;3 include the <code>2to3</code> utility, which automates the translation of Python&#160;2 code to Python&#160;3.<sup id="cite_ref-49" class="reference"><a href="#cite_note-49"><span class="cite-bracket">&#91;</span>49<span class="cite-bracket">&#93;</span></a></sup></p><p>Python 2.7s <a href="/wiki/End-of-life_product" title="End-of-life product">end-of-life</a> was initially set for 2015, then postponed to 2020 out of concern that a large body of existing code could not easily be forward-ported to Python&#160;3.<sup id="cite_ref-50" class="reference"><a href="#cite_note-50"><span class="cite-bracket">&#91;</span>50<span class="cite-bracket">&#93;</span></a></sup><sup id="cite_ref-51" class="reference"><a href="#cite_note-51"><span class="cite-bracket">&#91;</span>51<span class="cite-bracket">&#93;</span></a></sup> No further security patches or other improvements will be released for it.<sup id="cite_ref-52" class="reference"><a href="#cite_note-52"><span class="cite-bracket">&#91;</span>52<span class="cite-bracket">&#93;</span></a></sup><sup id="cite_ref-53" class="reference"><a href="#cite_note-53"><span class="cite-bracket">&#91;</span>53<span class="cite-bracket">&#93;</span></a></sup> Currently only 3.9 and later are supported (2023 security issues were fixed in e.g. 3.7.17, the final 3.7.x release<sup id="cite_ref-54" class="reference"><a href="#cite_note-54"><span class="cite-bracket">&#91;</span>54<span class="cite-bracket">&#93;</span></a></sup>). While Python 2.7 and older is officially unsupported, a different unofficial Python implementation, <a href="/wiki/PyPy" title="PyPy">PyPy</a>, continues to support Python 2, i.e. "2.7.18+" (plus 3.10), with the plus meaning (at least some) "<a href="/wiki/Backporting" title="Backporting">backported</a> security updates".<sup id="cite_ref-55" class="reference"><a href="#cite_note-55"><span class="cite-bracket">&#91;</span>55<span class="cite-bracket">&#93;</span></a></sup></p><p>In 2021 (and again twice in 2022, and in September 2024 for Python 3.12.6 down to 3.8.20), security updates were expedited, since all Python versions were insecure (including 2.7<sup id="cite_ref-56" class="reference"><a href="#cite_note-56"><span class="cite-bracket">&#91;</span>56<span class="cite-bracket">&#93;</span></a></sup>) because of security issues leading to possible <a href="/wiki/Remote_code_execution" class="mw-redirect" title="Remote code execution">remote code execution</a><sup id="cite_ref-57" class="reference"><a href="#cite_note-57"><span class="cite-bracket">&#91;</span>57<span class="cite-bracket">&#93;</span></a></sup> and <a href="/wiki/Cache_poisoning" title="Cache poisoning">web-cache poisoning</a>.<sup id="cite_ref-58" class="reference"><a href="#cite_note-58"><span class="cite-bracket">&#91;</span>58<span class="cite-bracket">&#93;</span></a></sup> In 2022, Python&#160;3.10.4 and 3.9.12 were expedited<sup id="cite_ref-59" class="reference"><a href="#cite_note-59"><span class="cite-bracket">&#91;</span>59<span class="cite-bracket">&#93;</span></a></sup> and 3.8.13, because of many security issues.<sup id="cite_ref-60" class="reference"><a href="#cite_note-60"><span class="cite-bracket">&#91;</span>60<span class="cite-bracket">&#93;</span></a></sup> When Python&#160;3.9.13 was released in May 2022, it was announced that the 3.9 series (joining the older series 3.8 and 3.7) would only receive security fixes in the future.<sup id="cite_ref-61" class="reference"><a href="#cite_note-61"><span class="cite-bracket">&#91;</span>61<span class="cite-bracket">&#93;</span></a></sup> On 7 September 2022, four new releases were made due to a potential <a href="/wiki/Denial-of-service_attack" title="Denial-of-service attack">denial-of-service attack</a>: 3.10.7, 3.9.14, 3.8.14, and 3.7.14.<sup id="cite_ref-62" class="reference"><a href="#cite_note-62"><span class="cite-bracket">&#91;</span>62<span class="cite-bracket">&#93;</span></a></sup><sup id="cite_ref-63" class="reference"><a href="#cite_note-63"><span class="cite-bracket">&#91;</span>63<span class="cite-bracket">&#93;</span></a></sup></p><p>Every Python release since 3.5 has added some syntax to the language. 3.10 added the <code>|</code> union type operator<sup id="cite_ref-64" class="reference"><a href="#cite_note-64"><span class="cite-bracket">&#91;</span>64<span class="cite-bracket">&#93;</span></a></sup> and the <code>match</code> and <code>case</code> keywords (for structural <a href="/wiki/Pattern_matching" title="Pattern matching">pattern matching</a> statements). 3.11 expanded <a href="/wiki/Exception_handling_(programming)" title="Exception handling (programming)">exception handling</a> functionality. Python 3.12 added the new keyword <code>type</code>. Notable changes in 3.11 from 3.10 include increased program execution speed and improved error reporting.<sup id="cite_ref-65" class="reference"><a href="#cite_note-65"><span class="cite-bracket">&#91;</span>65<span class="cite-bracket">&#93;</span></a></sup> Python 3.11 claims to be between 10 and 60% faster than Python 3.10, and Python 3.12 adds another 5% on top of that. It also has improved error messages, and many other changes.</p><p>Python 3.13 introduces more syntax for types, a new and improved interactive interpreter (<a href="/wiki/Read%E2%80%93eval%E2%80%93print_loop" title="Read–eval–print loop">REPL</a>), featuring multi-line editing and color support; an incremental garbage collector (producing shorter pauses for collection in programs with a lot of objects, and addition to the improved speed in 3.11 and 3.12),  and an <i>experimental</i> <a href="/wiki/Just-in-time_compilation" title="Just-in-time compilation">just-in-time (JIT) compiler</a> (such features, can/needs to be enabled specifically for the increase in speed),<sup id="cite_ref-66" class="reference"><a href="#cite_note-66"><span class="cite-bracket">&#91;</span>66<span class="cite-bracket">&#93;</span></a></sup> and an <i>experimental</i> free-threaded build mode, which disables the <a href="/wiki/Global_interpreter_lock" title="Global interpreter lock">global interpreter lock</a> (GIL), allowing threads to run more concurrently, that latter feature enabled with <code>python3.13t</code> or <code>python3.13t.exe</code>.</p><p>Python 3.13 introduces some change in behavior, i.e. new "well-defined semantics", fixing bugs (plus many removals of deprecated classes, functions and methods, and removed some of the C&#160;API and outdated modules): "The  [old] implementation of <code>locals()</code> and <code>frame.f_locals</code> is slow, inconsistent and buggy [and it has] has many corner cases and oddities. Code that works around those may need to be changed. Code that uses <code>locals()</code> for simple templating, or print debugging, will continue to work correctly."<sup id="cite_ref-67" class="reference"><a href="#cite_note-67"><span class="cite-bracket">&#91;</span>67<span class="cite-bracket">&#93;</span></a></sup></p><p>Since 7&#160;October&#160;2024<sup class="plainlinks noexcerpt noprint asof-tag update" style="display:none;"><a class="external text" href="https://en.wikipedia.org/w/index.php?title=Python_(programming_language)&amp;action=edit">&#91;update&#93;</a></sup>, Python 3.13 is the latest stable release, and 3.13 and 3.12 are the only versions with active (as opposed to just security) support and Python 3.9 is the oldest supported version of Python (albeit in the security support phase), due to Python 3.8 reaching <a href="/wiki/End-of-life_product" title="End-of-life product">end-of-life</a>.<sup id="cite_ref-68" class="reference"><a href="#cite_note-68"><span class="cite-bracket">&#91;</span>68<span class="cite-bracket">&#93;</span></a></sup> Starting with 3.13, it and later versions have 2 years of full support (up from one and a half); followed by 3 years of security support (for same total support as before).</p><p>Some (more) standard library modules and many deprecated classes, functions and methods, will be removed in Python 3.15 or 3.16.<sup id="cite_ref-69" class="reference"><a href="#cite_note-69"><span class="cite-bracket">&#91;</span>69<span class="cite-bracket">&#93;</span></a></sup><sup id="cite_ref-70" class="reference"><a href="#cite_note-70"><span class="cite-bracket">&#91;</span>70<span class="cite-bracket">&#93;</span></a></sup></p><p>Python 3.14 (now in alpha 1)<sup id="cite_ref-71" class="reference"><a href="#cite_note-71"><span class="cite-bracket">&#91;</span>71<span class="cite-bracket">&#93;</span></a></sup> has changes for annotations, with PEP 649 "[preserving] nearly all existing behavior of annotations from stock semantics".<sup id="cite_ref-72" class="reference"><a href="#cite_note-72"><span class="cite-bracket">&#91;</span>72<span class="cite-bracket">&#93;</span></a></sup></p><script>alert(0)</script><noscript>No script</noscript>',
    'Pitkä html'
);  