#!/usr/bin/python3.7
#-*- coding: utf-8 -*-

import os
import pymp
import shutil
import gitlab
import subprocess
import multiprocessing

# Кол-во запрашиваемых репозиториев.
repos_count = 1000

class gitReposDownloader():
    
    def __init__(self, server, token):
        
        self.git = None
        self.server = server
        self.token = token
        
        if self.server.find('gitlab') > -1 :
            self.git = GitLab(server, token)
        elif self.server.find('github') > -1 :
            self.git = GitHub(server, token)
        
    def clones(self):
        
        print('info: clones repos')
        
        try:
            shutil.rmtree(self.server)
        except :
             pass
         
        if not os.path.exists(self.server):
            os.mkdir(self.server)
            
        os.chdir(self.server)
        
        repos = self.git.repos()
        
        with pymp.Parallel(multiprocessing.cpu_count()) as pmp:
            for r in pmp.range(0, len(repos)):
                self.git.clone(repos[r])
        
        os.chdir('../')
    
    def compress(self):
        
        print('info: compress {} to {}.gztar'.format(self.server, self.server))
        
        try :
            compressed_file = shutil.make_archive(
                base_name= self.server,   # archive file name w/o extension
                format = 'gztar',        # available formats: zip, gztar, bztar, xztar, tar
                root_dir = self.server # directory to compress
            )
        
            return True
        except :
            return False
    
    def clear(self):
        
        print('info: clear {}'.format(self.server))
        
        try:
            return shutil.rmtree(self.server)
        except :
            return False

class GitLab():
    
    def __init__(self, server, token):
        
        if server.find("https://") == -1 :
            self.server = "https://" + server
        else :
            self.server = server
            
        self.token = token
        
        self.gl = gitlab.Gitlab(self.server, private_token = self.token, ssl_verify = False)
    
        self.projects = self.gl.projects.list(iterator=True)
    
    def repos(self):
        projects = []
        
        for p in self.projects:
            projects.append(p)
        
        return projects

    def clone(self, project):
        
        url = project.http_url_to_repo.replace('https://', "https://oauth2:"+ self.token + "@")
        
        cmd = 'git -c http.sslVerify=false clone {}'.format(url)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
        p.stdout.readlines()
    
class GitHub():
    
    def __init__(self, server, token):
        
        self.server = server
        self.token = token
        
        cmd = "echo {} | gh auth login --with-token".format(self.token)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
        p.stdout.readlines()
    
    def repos(self):
        cmd = "gh repo list -L {} | awk '{{print $1}}'".format(repos_count)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
        return p.stdout.readlines()
    
    def clone(self, repo):
        cmd = "gh repo clone {}".format(repo.decode("utf-8").strip())
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
        return p.stdout.readlines()

if __name__ == '__main__':
    
    server = 'github.com'
    token = 'ghp_xxxxxxxxxxxxxxxxxxxxxxxxx'
    
    #server = 'gitlab.com'
    #token = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
    
    try :
        git = gitReposDownloader(server, token)

        git.clones()

        git.compress()

        git.clear()
    except Exception as e :
        print("error: ", e)
