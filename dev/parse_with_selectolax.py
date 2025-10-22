"""
Example of parsing PyPI Inspector HTML content with selectolax
Copy the relevant parts into your Jupyter notebook cells
"""

# First, install selectolax if not already installed:
# !pip install selectolax

from selectolax.parser import HTMLParser

# Parse the HTML content
def parse_pypi_inspector(content):
    """
    Parse PyPI Inspector HTML content and extract version information
    
    Args:
        content: HTML string from utils.fetch_content()
    
    Returns:
        list of dicts with version info
    """
    tree = HTMLParser(content)
    
    # Find all table rows (skip header)
    rows = tree.css('table tr')
    
    versions = []
    for row in rows[1:]:  # Skip header row
        cells = row.css('td')
        if len(cells) >= 3:
            # Extract version link and text
            version_link = cells[0].css_first('a')
            version = version_link.text() if version_link else None
            version_url = version_link.attributes.get('href', '') if version_link else None
            
            # Extract timestamp
            timestamp = cells[1].text()
            
            # Extract artifacts count
            artifacts = cells[2].text()
            
            versions.append({
                'version': version,
                'url': version_url,
                'timestamp': timestamp,
                'artifacts': int(artifacts) if artifacts.isdigit() else artifacts
            })
    
    return versions


# Example usage with your code:
# content = utils.fetch_content(PYPI_INSPECTOR_URL + "liburlparser/")
# versions = parse_pypi_inspector(content)
# 
# # Display results
# for v in versions:
#     print(f"Version {v['version']}: {v['timestamp']} ({v['artifacts']} artifacts)")


# Alternative: Extract specific elements
def extract_elements_example(content):
    """
    Examples of different selectolax queries you can use
    """
    tree = HTMLParser(content)
    
    # Get page title
    title = tree.css_first('title')
    print(f"Title: {title.text() if title else 'Not found'}")
    
    # Get all links
    links = tree.css('a')
    print(f"\nFound {len(links)} links:")
    for link in links[:5]:  # Show first 5
        print(f"  - {link.text()}: {link.attributes.get('href', '')}")
    
    # Get specific element by ID
    loading_error = tree.css_first('#loading-error')
    if loading_error:
        print(f"\nLoading error message: {loading_error.text()}")
    
    # Get elements by class
    noscript_content = tree.css('.noscript-content')
    if noscript_content:
        print(f"\nNoscript elements found: {len(noscript_content)}")
    
    # Get table data
    table = tree.css_first('table')
    if table:
        print("\nTable found!")
        headers = [th.text() for th in table.css('th')]
        print(f"Headers: {headers}")
    
    return tree


# For the actual PyPI Inspector page (not the client challenge page):
def parse_real_pypi_page(html_str):
    """
    Parse the actual PyPI Inspector page with version table
    (like the html_str in cell 8 of your notebook)
    """
    tree = HTMLParser(html_str)
    
    # Extract project name from input field
    project_input = tree.css_first('input[name="project"]')
    project_name = project_input.attributes.get('value', '') if project_input else None
    
    # Extract version count message
    version_msg = tree.css_first('p')
    version_count_text = version_msg.text() if version_msg else None
    
    # Extract all versions from table
    versions = []
    for row in tree.css('table tbody tr, table tr'):
        cells = row.css('td')
        if len(cells) >= 3:
            version_link = cells[0].css_first('a')
            if version_link:
                versions.append({
                    'version': version_link.text().strip(),
                    'url': version_link.attributes.get('href', ''),
                    'timestamp': cells[1].text().strip(),
                    'artifacts': cells[2].text().strip()
                })
    
    return {
        'project': project_name,
        'version_count': version_count_text,
        'versions': versions
    }


if __name__ == '__main__':
    # Test with the html_str from your notebook
    html_str = """<html><body>
    <main>
      <h1><a href="/">Inspector</a></h1>
      <form action="/">
          <input type="text" name="project" placeholder="Project name" value="liburlparser" autocomplete="off">
        <input type="submit">
      </form><p>Retrieved 20 versions.</p>

<table>
<colgroup>
  <col style="width: 160px">
  <col style="width: 160px">
  <col style="width: 160px">
</colgroup>
<thead>
<tr>
  <th>Version</th>
  <th>Upload Timestamp</th>
  <th>Artifacts</th>
</tr>
</thead>
  <tr>
    <td><a href="./1.6.0">1.6.0</a></td>
    <td>2025-05-04T13:21:22</td>
    <td>10</td>
  </tr>
  <tr>
    <td><a href="./1.5.0">1.5.0</a></td>
    <td>2024-10-18T18:22:29</td>
    <td>31</td>
  </tr>
</table>
    </main>
  </body>
</html>"""
    
    result = parse_real_pypi_page(html_str)
    print(f"Project: {result['project']}")
    print(f"Info: {result['version_count']}")
    print(f"\nVersions found: {len(result['versions'])}")
    for v in result['versions'][:5]:
        print(f"  {v['version']}: {v['timestamp']} ({v['artifacts']} artifacts)")
