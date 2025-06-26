import os
from pathlib import Path

def generate_html_tree(startpath, output_file='folder_tree.html'):
    root_name = os.path.basename(startpath)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Folder Structure</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        .tree {{
            margin-top: 20px;
        }}
        .folder {{
            font-weight: bold;
            color: #2980b9;
            cursor: pointer;
            padding: 2px 0;
        }}
        .folder::before {{
            content: "📁 ";
        }}
        .file {{
            color: #333;
            margin-left: 20px;
            padding: 2px 0;
            display: flex;
            align-items: center;
        }}
        .file::before {{
            content: "📄 ";
        }}
        .collapsible {{
            cursor: pointer;
            user-select: none;
        }}
        .collapsible::before {{
            content: "▶ ";
            font-size: 10px;
            color: #7f8c8d;
        }}
        .active::before {{
            content: "▼ ";
        }}
        .nested {{
            display: none;
            margin-left: 20px;
        }}
        .active + .nested {{
            display: block;
        }}
        .file-actions {{
            margin-left: 10px;
            display: inline-flex;
            gap: 5px;
        }}
        .btn {{
            padding: 2px 6px;
            font-size: 12px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            text-decoration: none;
        }}
        .btn-view {{
            background-color: #3498db;
            color: white;
        }}
        .btn-download {{
            background-color: #2ecc71;
            color: white;
        }}
        .btn:hover {{
            opacity: 0.8;
        }}
        .excluded {{
            color: #95a5a6;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <h1>Folder Structure: {root_name}</h1>
    <div class="tree">
"""

    def add_directory(path, level=0):
        nonlocal html
        indent = "    " * level
        name = os.path.basename(path)
        
        # Skip .git folders
        if name == '.git':
            html += f'{indent}<div class="excluded">(excluded: .git folder)</div>\n'
            return
            
        if os.path.isdir(path):
            html += f'{indent}<div class="folder collapsible">{name}</div>\n'
            html += f'{indent}<div class="nested">\n'
            try:
                # List directories first, then files
                items = sorted(os.listdir(path))
                dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
                files = [item for item in items if not os.path.isdir(os.path.join(path, item))]
                
                for item in dirs:
                    item_path = os.path.join(path, item)
                    add_directory(item_path, level + 1)
                
                for item in files:
                    item_path = os.path.join(path, item)
                    add_file(item_path, level + 1)
                    
            except PermissionError:
                html += f'{indent}<div class="excluded">(permission denied)</div>\n'
            html += f'{indent}</div>\n'
        else:
            add_file(path, level)

    def add_file(path, level):
        nonlocal html
        indent = "    " * level
        name = os.path.basename(path)
        relative_path = os.path.relpath(path, startpath)
        
        html += f'{indent}<div class="file">'
        html += f'<span>{name}</span>'
        html += f'<span class="file-actions">'
        html += f'<a href="{relative_path}" target="_blank" class="btn btn-view">View</a>'
        html += f'<a href="{relative_path}" download class="btn btn-download">Download</a>'
        html += '</span></div>\n'

    # Start the tree
    html += f'<div class="folder collapsible active">{root_name}</div>\n'
    html += '<div class="nested" style="display:block;">\n'
    
    # List directories first, then files
    items = sorted(os.listdir(startpath))
    dirs = [item for item in items if os.path.isdir(os.path.join(startpath, item)) and item != '.git']
    files = [item for item in items if not os.path.isdir(os.path.join(startpath, item))]
    
    for item in dirs:
        item_path = os.path.join(startpath, item)
        add_directory(item_path, 1)
    
    for item in files:
        item_path = os.path.join(startpath, item)
        add_file(item_path, 1)
    
    html += '</div>\n'
    
    html += """
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var coll = document.getElementsByClassName("collapsible");
            for (var i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.display === "block") {
                        content.style.display = "none";
                    } else {
                        content.style.display = "block";
                    }
                });
            }
            
            // Make the root folder expanded by default
            var rootFolder = document.querySelector('.tree > .folder');
            if (rootFolder) {
                rootFolder.classList.add('active');
                rootFolder.nextElementSibling.style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

# Usage - replace with your actual folder path
folder_path = os.getcwd()  # This will use the current working directory
generate_html_tree(folder_path)