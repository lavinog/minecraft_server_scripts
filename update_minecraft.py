#! /usr/bin/python3

import requests
import hashlib


class MinecraftUpdater(object):

    version_manifest_url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'

    def __init__(self):
        self.manifest_json = None
        self.latest_release_id = None
        self.latest_version_obj = None
        self.latest_version_json = None
        self.latest_server_obj = None

    def DoUpdate(self):
        print('Getting manifest...')
        self._get_manifest()
        if self.manifest_json:
            print('Parsing manifest...')
            self._parse_manifest()
        if self.latest_version_obj:
            print(''' id: {id}
 url: {url}
 time: {time}
 type: {type}
 releaseTime: {releaseTime}'''
                .format(**self.latest_version_obj))
            print('Getting lastest version info...')
            self._get_latest_version_info()


        if self.latest_server_obj:
            print(''' url: {url}
 sha1: {sha1}
 size: {size}'''
                .format(**self.latest_server_obj))
            self._download_version()



    def _get_manifest(self):
        r = requests.get(self.version_manifest_url)
        self.manifest_json = r.json()


    def _parse_manifest(self):
        self.latest_release_id = self.manifest_json['latest']['release']
        for ver in self.manifest_json['versions']:
            if ver['id'] == self.latest_release_id:
                self.latest_version_obj = ver
                break

    def _get_latest_version_info(self):
        r = requests.get(self.latest_version_obj['url'])
        self.latest_version_json = r.json()
        if self.latest_version_json:
            self.latest_server_obj = self.latest_version_json['downloads']['server']

    def _download_version(self):
        filename = 'server_{}.jar'.format(self.latest_release_id)
        sha1hasher = hashlib.sha1()
        print('Saving file to {}'.format( filename))
        r = requests.get(self.latest_server_obj['url'], stream=True)
        with open(filename, 'wb') as fout:
            for chunk in r.iter_content(chunk_size=128):
                fout.write(chunk)
                sha1hasher.update(chunk)
        self.download_sha1 = sha1hasher.hexdigest()
        print('Save complete')
        print('downloaded sha1: {}'.format(self.download_sha1))
        print('expected sha1: {}'.format( self.latest_server_obj['sha1']))
        if self.download_sha1 == self.latest_server_obj['sha1']:
            print('matches')
        else:
            print('Does NOT match!')


def main():
    MU = MinecraftUpdater()
    MU.DoUpdate()

if __name__ == '__main__':
    main()
