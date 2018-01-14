def not_found_wrap(ret):
    if ret:
        return { 'status': 'OK' }
    else:
        return { 'status': 'error', 'error': 'not_found' }

class Handler(object):
    def __init__(self, kodi):
        self.kodi = kodi

    def search_and_play_handler(self, video_filter):
        print('search_and_play_handler', video_filter)

        return not_found_wrap(self.kodi.find_and_play(video_filter))

    def next_handler(self):
        print('next_handler')
        return not_found_wrap(self.kodi.next_item())

    def previous_handler(self):
        print('previous_handler')
        return not_found_wrap(self.kodi.previous_item())

    def start_over_handler(self):
        print('start_over_handler')
        self.kodi.start_over()
        return { 'statuts': 'OK' }

    def pause_handler(self):
        print('pause_handler')
        self.kodi.pause()
        return { 'status': 'OK' }

    def resume_handler(self):
        print('resume_handler')
        self.kodi.resume()
        return { 'status': 'OK' }

    def stop_handler(self):
        print('stop_handler')
        self.kodi.stop()
        return { 'status': 'OK' }

    def handler(self, data):
        print('handler data:', data)
        responseData = { 'status': 'Not found' }
        if data['type'] == 'command':
            if data['commandType'] == 'searchAndPlay':
                responseData = search_and_play_handler(data['filter'])
            elif data['commandType'] == 'next':
                responseData = next_handler()
            elif data['commandType'] == 'previous':
                responseData = previous_handler()
            elif data['commandType'] == 'startOver':
                responseData = start_over_handler()
            elif data['commandType'] == 'pause':
                responseData = pause_handler()
            elif data['commandType'] == 'resume':
                responseData = resume_handler()
            elif data['commandType'] == 'stop':
                responseData = stop_handler()

        print('handler responseData:', responseData)

        return responseData