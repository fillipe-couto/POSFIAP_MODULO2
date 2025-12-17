unique_identifier = 'ms-python.vscode-pylance'
version = '2025.10.4'
target_platform = 'linux-x64'

publisher, package = unique_identifier.split('.')
url = (
    f'https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{package}/{version}/vspackage'
    + (f'?targetPlatform={target_platform}' if target_platform else ''))
print(url)