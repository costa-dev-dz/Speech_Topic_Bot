# Git Shortcuts
function gcp { 
    param($msg)
    git add .
    git commit -m $msg
    git push
}
function gs { git status }
function gl { git log --oneline -5 }