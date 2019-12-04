print colour.printHighlightedRed % "Build variant %s is not in the list of " \
                                                       "accepted build variants:" % self.config.buildVariant
                    for variant in acceptedBuildVariants:
                        print variant
                    print "To request a new variant, please file a request with QA"
                    sys.exit(1)

            print "Downloading App from Artifactory"
            session = requests.Session()
            session.auth = (self.config.gitHubUser, self.config.artifactoryToken)
            queryUrl = "https://artifactory-sjc.plex.bz/artifactory/api/search/aql"
            query = 'items.find({"repo":"%s", "@plex.source":"%s", "name":{"$match":"*%s.apk"}})' \
                    % (self.config.artifactoryAndroidRepo, self.config.buildBranch, self.config.buildVariant)
            request = session.post(queryUrl, data=query, headers={"content-type": "text/plain"})

            if request.status_code != requests.codes.ok:
                self.visual.printError("[BUILD FAILED] Artifactory couldn't be reached", log=self.buildLog)
                session.close()
                sys.exit(1)

            builds = request.json()
            latestBuild = builds['results'][-1]
            buildInfoFile = self.config.tempPath + 'KeplerApkInfo.json'
            downloadFile = True

            # check if we already have the latest version requested
            if self.runningClientAutomation:
                if os.path.isfile(buildInfoFile):
                    with open(self.config.tempPath + 'KeplerApkInfo.json') as jsonFile:
                        oldBuildInfo = json.load(jsonFile)

                    if oldBuildInfo['name'] == latestBuild['name']:
                        downloadFile = False
            else:
                if latestBuild['name'] in os.listdir(self.config.tempPath):
                    downloadFile = False

            if not downloadFile:
                self.visual.printMessage("Latest version (%s) already downloaded, so we won't download it again"
                                         % latestBuild['name'], log=self.buildLog)
                return

            self.config.appVersion = latestBuild['path']
            self.config.gitHash = self.config.appVersion.split('-')[-1]

            self.buildLog.info("Downloading build %s" % self.config.appVersion)
            downloadUrl = "https://artifacts.plex.tv/%s/%s/%s" \
                          % (self.config.artifactoryAndroidRepo, self.config.appVersion, latestBuild['name'])
            request = session.get(downloadUrl)

            if request.status_code != requests.codes.ok:
                self.visual.printError("[BUILD FAILED] Artifactory download failed", log=self.buildLog)
                session.close()
                sys.exit(1)
            else:
                open(latestBuild['name'], 'wb').write(request.content)
                self.buildLog.info("Build downloaded successfully")
                session.close()

            if globalMethods.bool.runningClientAutomation(self.config):
                newFileName = 'Kepler.apk'
            else:
                newFileName = latestBuild['name']

            oldFilePath = self.config.rootPath + latestBuild['name']
            newFilePath = self.config.tempPath + newFileName
            os.rename(oldFilePath, newFilePath)

            # save new build's info
            with open(self.config.tempPath + 'KeplerApkInfo.json', 'w') as outfile:
                json.dump(latestBuild, outfile)

            buildSuccess = True

            if not self.runningClientAutomation:
                print "Build '%s' available in the QA temp folder (%s)" % (latestBuild['name'], self.config.tempPath)