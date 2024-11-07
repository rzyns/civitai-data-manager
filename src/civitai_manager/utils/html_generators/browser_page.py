from pathlib import Path
import json
from datetime import datetime

def generate_global_summary(output_dir, VERSION):
    """
    Generate an HTML summary of all models in the output directory
    
    Args:
        output_dir (Path): Directory containing the JSON files
        VERSION (str): Version of the script
    """
    try:
        # Find all model.json files
        model_files = list(Path(output_dir).glob('*/*/civitai_model.json')) + \
                      list(Path(output_dir).glob('*/*_civitai_model.json'))
        
        # Dictionary to store models by type
        models_by_type = {}
        
        for model_file in model_files:
            try:
                # Get paths for both model and version files
                base_name = model_file.parent.name
                version_file = model_file.parent / f"{base_name}_civitai_model_version.json"
        
                # Read both files
                with open(model_file, 'r', encoding='utf-8') as f:
                    model_data = json.load(f)

                version_data = {}
                if version_file.exists():
                    with open(version_file, 'r', encoding='utf-8') as f:
                        version_data = json.load(f)

                model_type = model_data.get('type', 'Unknown')
                
                if model_type not in models_by_type:
                    models_by_type[model_type] = []
                    
                models_by_type[model_type].append({
                    # Add model data
                    'name': model_data.get('name', 'Unknown'),
                    'creator': model_data.get('creator', {}).get('username', 'Unknown'),
                    'base_name': base_name,
                    'html_file': f"{base_name}.html",
                    'tags': model_data.get('tags', []),
                    # Add version data
                    'version_name': version_data.get('name', ''),
                    'downloads': version_data.get('stats', {}).get('downloadCount', 0),
                })
            except:
                continue

        # Sort each type's models by downloads
        for model_type in models_by_type:
            models_by_type[model_type].sort(key=lambda x: x['downloads'], reverse=True)

        # Create sections HTML for each type
        type_sections = ''
        total_models = sum(len(models) for models in models_by_type.values())
        
        for model_type, models in sorted(models_by_type.items()):
            type_sections += f"""
            <div class="type-section" data-type="{model_type.lower()}">
                <h2>{model_type} ({len(models)} models)</h2>
                <div class="models-grid">
                    {''.join(f"""
                    <div class="model-card" data-tags="{','.join(model['tags']).lower()}">
                        <h3><a href="{model['base_name']}/{model['html_file']}">{model['name']}</a></h3>
                        <small class="version-name">{model['version_name']}</small>
                        <div>by {model['creator']}</div>
                        <div class="downloads">Downloads: {model['downloads']:,}</div>
                        <div class="tags">
                            {''.join(f'<span class="tag">{tag}</span>' for tag in model['tags'])}
                        </div>
                    </div>
                    """ for model in models)}
                </div>
            </div>
            """

        # Update the HTML content with type sections
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Civitai Metadata Manager</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            font-size: 0.8rem;
            color: #666;
        }}
        .search-container {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .search-box {{
            width: 80%;
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 4px;
            margin-bottom: 10px;
        }}
        .models-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }}
        .model-card {{
            background-color: #f8f9fa;
            border: 1px solid #eee;
            border-radius: 8px;
            padding: 15px;
            transition: transform 0.2s;
        }}
        .model-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .downloads {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-top: 10px;
        }}
        .tag {{
            background-color: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
        }}
        h1 {{
            color: #2c3e50;
        }}
        h3 {{
            margin: 0;
        }}
        .version-name {{
            margin-top: -5px;
            display: block;
        }}
        .hidden {{
            display: none !important;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            color: #2779af;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="search-container">
            <h1>Civitai Metadata Manager</h1>
            <br />
            <h2>({total_models} models)</h2>

            <input type="text" class="search-box" id="searchBox" placeholder="Search by tags (comma separated)...">
        </div>
        {type_sections}
    </div>

    <div class="footer">
        Civitai Metadata Manager. Version {VERSION}. <a href="https://github.com/jeremysltn/civitai-metadata-manager">GitHub</a>
        <br />
        Generated: {datetime.now().isoformat()}
    </div>

    <script>
        const searchBox = document.getElementById('searchBox');
        const modelCards = document.querySelectorAll('.model-card');

        searchBox.addEventListener('input', function() {{
            const searchTags = searchBox.value.toLowerCase().split(',').map(tag => tag.trim()).filter(tag => tag);
            
            modelCards.forEach(card => {{
                if (!searchTags.length) {{
                    card.classList.remove('hidden');
                    return;
                }}
                
                const cardTags = card.dataset.tags.split(',');
                const matchesSearch = searchTags.every(searchTag => 
                    cardTags.some(cardTag => cardTag.includes(searchTag))
                );
                
                if (matchesSearch) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            // Show/hide section headers based on visible cards
            document.querySelectorAll('.type-section').forEach(section => {{
                const visibleCards = section.querySelectorAll('.model-card:not(.hidden)').length;
                section.style.display = visibleCards > 0 ? 'block' : 'none';
            }});
        }});
    </script>
</body>
</html>
"""

        # Write the summary file
        summary_path = Path(output_dir) / 'models_manager.html'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\nGlobal summary generated: {summary_path}")
        return True

    except Exception as e:
        print(f"Error generating global summary: {str(e)}")
        return False