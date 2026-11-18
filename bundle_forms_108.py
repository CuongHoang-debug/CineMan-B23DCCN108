import os

uml_dir = r'C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\uml_108'

def combine(files, out_file):
    parts = []
    for f in files:
        path = os.path.join(uml_dir, f)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as infile:
                parts.append(f"' ===== {f} =====\n" + infile.read().strip())
    content = '\n\n'.join(parts)
    out_path = os.path.join(uml_dir, out_file)
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(content)
    print(f"Wrote {out_file} ({len(content)} chars)")

combine(['01_usecase_tongquan_108.puml', '02_usecase_chitiet_dangky_108.puml', '03_usecase_chitiet_banve_108.puml'], 'cineman_form_dacta_108.puml')

combine([
    '04_entity_class_diagram_108.puml',
    '05_analysis_class_banve_108.puml',
    '06_communication_banve_108.puml',
    '07_sequence_analysis_banve_108.puml',
    '14_analysis_class_dangky_108.puml',
    '15_communication_dangky_108.puml',
    '16_sequence_analysis_dangky_108.puml'
], 'cineman_form_phantich_108.puml')

combine([
    '08_database_schema_108.puml',
    '09_design_class_banve_108.puml',
    '10_activity_banve_108.puml',
    '11_sequence_design_banve_108.puml',
    '17_design_class_dangky_108.puml',
    '18_activity_dangky_108.puml',
    '19_sequence_design_dangky_108.puml',
    '12_package_diagram_108.puml',
    '13_deployment_diagram_108.puml'
], 'cineman_form_thietke_108.puml')
