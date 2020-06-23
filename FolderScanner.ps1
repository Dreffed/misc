# powershell folder scanner tool
function Scan-Folder{
    [CmdletBinding(DefaultParameterSetName = 'ByPath')]
    param(
        [Parameter(Mandatory, ValueFromPipelineByPropertyName, ParameterSetName = 'ByPath')]
        [string]$Path
        
    )

    ## body opf the function...
    if ($Path){
        Get-ChildITem -Path $Path
    }
}

## run the code
Get-Location | Scan-Folder

