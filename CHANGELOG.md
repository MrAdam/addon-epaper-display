# Changelog

## [0.8.3](https://github.com/MrAdam/addon-epaper-display/compare/v0.8.2...v0.8.3) (2026-04-22)


### Bug Fixes

* **config:** fall back to supervisor API when TZ env var is absent ([94bbf5e](https://github.com/MrAdam/addon-epaper-display/commit/94bbf5e577fddcebfc1fb86da864c3e0c44eec9b))
* **config:** fall back to supervisor API when TZ env var is absent ([d5a6bf1](https://github.com/MrAdam/addon-epaper-display/commit/d5a6bf18a9e07524346f664b44979d685cfbe4fb))

## [0.8.2](https://github.com/MrAdam/addon-epaper-display/compare/v0.8.1...v0.8.2) (2026-04-22)


### Bug Fixes

* **config:** read timezone from TZ env var instead of supervisor HTTP API ([975f242](https://github.com/MrAdam/addon-epaper-display/commit/975f242c22248dbe4eff0db7559cff0dda572cf8))
* **config:** read timezone from TZ env var instead of supervisor HTTP API ([82b0f8a](https://github.com/MrAdam/addon-epaper-display/commit/82b0f8a2a89c84f6e78a8794b01215f6f5858a7a))

## [0.8.1](https://github.com/MrAdam/addon-epaper-display/compare/v0.8.0...v0.8.1) (2026-04-22)


### Bug Fixes

* **addon:** enable homeassistant_api to allow supervisor timezone fetch ([53778e1](https://github.com/MrAdam/addon-epaper-display/commit/53778e14132e9a2e0f7d645044ec75e647299c2c))
* **capture:** grant homeassistant_api permission for supervisor timezone fetch ([de2acc2](https://github.com/MrAdam/addon-epaper-display/commit/de2acc28a23cbf076dad153f55ded687bb23d028))
* **config:** log supervisor timezone fetch failures for debugging ([04968dc](https://github.com/MrAdam/addon-epaper-display/commit/04968dcab954128b0b0245a596f42fd9219fbdea))

## [0.8.0](https://github.com/MrAdam/addon-epaper-display/compare/v0.7.0...v0.8.0) (2026-04-22)


### Features

* **capture:** auto-detect timezone from HA supervisor ([aeeaa31](https://github.com/MrAdam/addon-epaper-display/commit/aeeaa312d657007ff0220bdb23ac40d0e3b88bad))
* **capture:** auto-detect timezone from HA supervisor ([a9646bb](https://github.com/MrAdam/addon-epaper-display/commit/a9646bbe8f95b108db78abe7e5138857a77a360e))

## [0.7.0](https://github.com/MrAdam/addon-epaper-display/compare/v0.6.0...v0.7.0) (2026-04-22)


### Features

* **capture:** add hide_toolbar option ([c67d7aa](https://github.com/MrAdam/addon-epaper-display/commit/c67d7aa57f2988abc385ad9688a95820f7ebb34a))
* **capture:** add hide_toolbar option ([abbebfc](https://github.com/MrAdam/addon-epaper-display/commit/abbebfc16a8cd615251fa3fd8a42f81c69383a1d))
* **examples:** add cron setup instructions and change default interval to 15 min ([38677cf](https://github.com/MrAdam/addon-epaper-display/commit/38677cf79dde31c17bb5622dfae03f8eb2917636))
* **examples:** add cron setup instructions and change default interval to 15 minutes ([03e695c](https://github.com/MrAdam/addon-epaper-display/commit/03e695c5becb280c924cb8d7eaeb843741664a3a))


### Bug Fixes

* **capture:** remove theme config option ([1759c3f](https://github.com/MrAdam/addon-epaper-display/commit/1759c3f7622013ea4b59b097dcf829e9f406978c))
* **capture:** remove theme config option ([043204b](https://github.com/MrAdam/addon-epaper-display/commit/043204bef0c472b56de0d8fa4eeb17cf38a9208b))
* **ci:** use toml+jsonpath to update uv.lock version in release-please ([6d4fac5](https://github.com/MrAdam/addon-epaper-display/commit/6d4fac53d9993eb35106a45226cec66dea5c2dcd))
* **ci:** use toml+jsonpath to update uv.lock version in release-please ([d6b384a](https://github.com/MrAdam/addon-epaper-display/commit/d6b384a44ae6411ed51aab0741cad5a4bc794c85))

## [0.6.0](https://github.com/MrAdam/addon-epaper-display/compare/v0.5.2...v0.6.0) (2026-04-22)


### Features

* add add-on icon ([8e5f54a](https://github.com/MrAdam/addon-epaper-display/commit/8e5f54a547e75de24addb58dd8415df28137d5c8))
* add add-on icon (Phosphor article, MIT) ([f91b33e](https://github.com/MrAdam/addon-epaper-display/commit/f91b33e808d68f96c15ee044613fa8b615142a4c))


### Bug Fixes

* **capture:** fix HA auth and rewrite wait logic ([714a3be](https://github.com/MrAdam/addon-epaper-display/commit/714a3bed7a11c78e9e764a7863b087fb8ca139ab))
* **capture:** fix HA auth, wait logic, and uv.lock CI ([addc487](https://github.com/MrAdam/addon-epaper-display/commit/addc487246736dca3a8ebd47f6d5d31961e4689e))
* **capture:** revert to wait_until=load, add auth sanity check, drop stage comments ([2aac06e](https://github.com/MrAdam/addon-epaper-display/commit/2aac06ed13f27782fdcbf3193b222a95edd4b6f2))


### Documentation

* **agents:** add local testing instructions for take_screenshot ([36efe76](https://github.com/MrAdam/addon-epaper-display/commit/36efe76838dddc96e67cd2de9ef1936cdf8aa732))
* **agents:** note --platform linux/amd64 needed on Apple Silicon ([c58a2f7](https://github.com/MrAdam/addon-epaper-display/commit/c58a2f7d3924049e6c7d218599d971d196dbf6fd))
* **agents:** replace local Python test with Docker-based testing instructions ([7f8bef7](https://github.com/MrAdam/addon-epaper-display/commit/7f8bef735a384b71e10e8e086fc6153a2e4e7e7b))

## [0.5.2](https://github.com/MrAdam/addon-epaper-display/compare/v0.5.1...v0.5.2) (2026-04-22)


### Bug Fixes

* **capture:** convert expires to milliseconds for HA frontend ([980243a](https://github.com/MrAdam/addon-epaper-display/commit/980243a9b7c12c41c587e8caf5f5d0b56a6ae8ac))
* **capture:** convert token expires to milliseconds ([b96fbd8](https://github.com/MrAdam/addon-epaper-display/commit/b96fbd8b3e33f277c0f1ae10af7c152dfb88332a))

## [0.5.1](https://github.com/MrAdam/addon-epaper-display/compare/v0.5.0...v0.5.1) (2026-04-22)


### Bug Fixes

* **capture:** drop hassUrl and clientId from hassTokens injection ([2e5e8a2](https://github.com/MrAdam/addon-epaper-display/commit/2e5e8a2df404973667e069e96707a2e2cb17290d))
* **capture:** drop hassUrl/clientId from hassTokens to fix connection error ([5eadeb6](https://github.com/MrAdam/addon-epaper-display/commit/5eadeb663916e77eb75ae93167347bd7c4a7fb5c))

## [0.5.0](https://github.com/MrAdam/addon-epaper-display/compare/v0.4.0...v0.5.0) (2026-04-22)


### Features

* **capture:** add theme option to set HA theme per capture ([604bcd0](https://github.com/MrAdam/addon-epaper-display/commit/604bcd04a68d6a4ec93d3acaf609503b6bab2491))
* **capture:** add theme option to set HA theme per capture ([9d807fb](https://github.com/MrAdam/addon-epaper-display/commit/9d807fb60db1e2c9634c7cd071c3d0fc73dfcd3b))


### Bug Fixes

* **capture:** correct hassTokens format to include hassUrl and clientId ([929cd9c](https://github.com/MrAdam/addon-epaper-display/commit/929cd9c5a4fa5f08f914d3a729f536b261d593bb))
* **capture:** correct hassTokens localStorage format for HA auth ([536ef1d](https://github.com/MrAdam/addon-epaper-display/commit/536ef1d221644319d46691215a3458816607f85f))
* **capture:** use calculated expiry instead of hardcoded far-future value ([f2ca402](https://github.com/MrAdam/addon-epaper-display/commit/f2ca402fea05b9ee767668e73736cf3b291e8620))

## [0.4.0](https://github.com/MrAdam/addon-epaper-display/compare/v0.3.0...v0.4.0) (2026-04-22)


### Features

* add translations for human-friendly option display names ([3ac2a95](https://github.com/MrAdam/addon-epaper-display/commit/3ac2a95fca425525176c2c033d2fce89bcb67655))
* add translations for human-friendly option display names ([7a4c343](https://github.com/MrAdam/addon-epaper-display/commit/7a4c343445d5dd591f82345eb5120db89d4172a1))
* **examples:** rewrite Pi client script with uv shebang and error screen ([7b16310](https://github.com/MrAdam/addon-epaper-display/commit/7b1631015f30ae36943d0d9efcdb6111efd5f13b))


### Bug Fixes

* **capture:** use add_init_script to set localStorage before navigation ([0983622](https://github.com/MrAdam/addon-epaper-display/commit/098362277b2cbee13c2c1b71933d484a701a1ddf))
* **capture:** use add_init_script to set localStorage, rewrite Pi example ([21af991](https://github.com/MrAdam/addon-epaper-display/commit/21af9917e3a533faaaf5534a5a021937824dc62d))


### Documentation

* **agents:** keep translations/en.yaml in sync with config.yaml options ([b8863c1](https://github.com/MrAdam/addon-epaper-display/commit/b8863c1d0c699e72694f98976c91d96db05d7aa1))

## [0.3.0](https://github.com/MrAdam/addon-epaper-display/compare/v0.2.0...v0.3.0) (2026-04-22)


### Features

* add repository.json for Supervisor add-on store ([6e81863](https://github.com/MrAdam/addon-epaper-display/commit/6e81863e65161b9bb281bc64afd9841b29a8a05e))
* add repository.json for Supervisor add-on store ([3157a00](https://github.com/MrAdam/addon-epaper-display/commit/3157a00d3a4264ab30b2d41d0262676f984a497e))


### Bug Fixes

* **ci:** use PAT for release-please to trigger CI on release PRs ([34c2c8c](https://github.com/MrAdam/addon-epaper-display/commit/34c2c8cf6727cc375c9084b22c8b5f21dd8881db))
* **ci:** use PAT for release-please to trigger CI on release PRs ([dd4056f](https://github.com/MrAdam/addon-epaper-display/commit/dd4056f2a9ff280b7d677f65ba6f58f716d2d47c))


### Documentation

* **agents:** add examples folder naming convention ([732ec44](https://github.com/MrAdam/addon-epaper-display/commit/732ec4470a9e95756911b1cd031ef3eb52837f57))
* **agents:** always use branches, never commit to main ([4455c48](https://github.com/MrAdam/addon-epaper-display/commit/4455c485d54528e8eef8b255140c6ce0dfee373a))

## [0.2.0](https://github.com/MrAdam/addon-epaper-display/compare/v0.1.0...v0.2.0) (2026-04-22)


### Features

* **capture:** add sidebar hiding and smarter HA wait strategy ([8cdfc7f](https://github.com/MrAdam/addon-epaper-display/commit/8cdfc7f838d94a796ce652f8ddba33f2b951bdcc))


### Documentation

* **agents:** document release-please versioning process ([7075706](https://github.com/MrAdam/addon-epaper-display/commit/70757061c4fd8d482050b227dd702c8e9d421bb3))
* **examples:** add Raspberry Pi Zero 2 W + Waveshare EPD 7.5" V2 companion script ([82b8223](https://github.com/MrAdam/addon-epaper-display/commit/82b822371e607bbd3195c112f9b1442cba894ec3))
* **examples:** remove fonts-noto prerequisite ([554e862](https://github.com/MrAdam/addon-epaper-display/commit/554e862add90a75dde5ee74ad08c23622c734bed))
* replace Pi-specific language with generic client terminology ([edbb5cf](https://github.com/MrAdam/addon-epaper-display/commit/edbb5cfb514e9118acf8190481de92410a8b0a80))
