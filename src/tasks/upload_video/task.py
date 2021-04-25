
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time,random



class  facebookVideoUpload:
        def __init__(self) -> None:
                self.driver = webdriver.Firefox(executable_path="bin/geckodriver.exe")
                self.driver.get("https://business.facebook.com/creatorstudio/home")
                self.login_button =self.locateElement("/html/body/div/div[1]/div[2]/div/div[2]/div/div/div/div[2]/div/div")
                self.login_button.click()
        def locateElement(self,xpath):
                try:
                        element = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,xpath)))
                except:
                        raise Exception(f"Button not found on Xpath: {xpath}")
                return element

        def locateElements(self,xpath):
                ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
                try:
                        elements = WebDriverWait(self.driver,10,ignored_exceptions=ignored_exceptions).until(EC.presence_of_all_elements_located((By.XPATH,xpath)))
                except:
                        raise Exception(f"Buttons not found on Xpath: {xpath}")
                return elements
        def locateElementCSS(self,css):
                try:
                        element = WebDriverWait(self.driver,25).until(EC.presence_of_element_located((By.CSS_SELECTOR,css)))
                except:
                        raise Exception(f"Button not found on CSS selector: {css}")
                return element

        def locateElementsCSS(self,css):
                ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
                try:
                        elements = WebDriverWait(self.driver,10,ignored_exceptions=ignored_exceptions).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,css)))
                except:
                        raise Exception(f"Buttons not found on Xpath: {xpath}")
                return elements
        def checkText(self,xpath,text):
                try:
                        WebDriverWait(self.driver,20).until(EC.text_to_be_present_in_element((By.XPATH,xpath),text))
                except:
                        raise Exception(f"Text not found on Xpath: {xpath}")
                

        def login(self,email,password):
                self.email_button = self.locateElement("//*[@id=\"email\"]")
                self.password_button = self.locateElement("//*[@id=\"pass\"]")
                self.email_button.send_keys(email)
                self.password_button.send_keys(password)
                self.send_credentials = self.locateElement("//*[@id=\"loginbutton\"]")
                self.send_credentials.click()

        def startUpload(self,videopath,pageName):

                try:
                        upload_single_video = self.locateElementCSS("input[accept='video/*, video/x-m4v, video/webm, video/x-ms-wmv, video/x-msvideo, video/3gpp, video/flv, video/x-flv, video/mp4, video/quicktime, video/mpeg, video/ogv, .ts, .mkv'][type='file']")
                        upload_single_video.send_keys(videopath)

                except:
                        raise Exception("css uploader selector changed!! or video not found")

                self.pages_list = self.locateElements("/html/body/div[4]/div/div/div/div[1]/div/div[2]/div/div[2]/div/*")
                                                        

                for page in self.pages_list:
                        if page.text == pageName:
                                page.click()
                                break
        def title_description_tags(self,title,description,tags):
                
                self.title_text = self.locateElementCSS("input[type='text'][placeholder='Add a title for your video here...']")
                # TODO ESTE DE ABAJO SI ES, .notranslate > div:nth-child(1) ESTE ES SU SELECTOR CSS Y EL HTML div data-contents = 'true'
                self.description_text = self.locateElementCSS(".notranslate")
                                                           
                                                            
                self.tags_text = self.locateElementCSS("input[aria-label='Add keywords to help people find your video']")
                
                self.title_text.send_keys(title)
                self.description_text.send_keys(description)
                for tag in tags:
                        self.tags_text.send_keys(tag)
                        time.sleep(2)
                        self.tags_text.send_keys(Keys.ARROW_UP)
                        self.tags_text.send_keys(Keys.RETURN)
                        time.sleep(2)
        def addThumbnail(self,thumbnailPath):

                thumbnailButtonChildren = self.locateElementCSS("div[loadingindicatorstyle='none'][style='width: 128px; height: 72px;']")
                thumbnailButton =  WebDriverWait(thumbnailButtonChildren,10).until(EC.element_to_be_clickable((By.XPATH,'..')))
                thumbnailButton.click()
                try:
                        upload_single_video = self.locateElementCSS("input[accept='.png,.jpg,.jpeg'][type='file']")
    
                        upload_single_video.send_keys(thumbnailPath)

                except:
                        raise Exception("css thumbnail selector changed!! or thumbnail not found")


        def publishVideo(self,publishNow=True,date=None,playlistName=''):

                self.publishOptions = self.locateElement("//div[contains(text(), '2. Publishing Options')]")
                self.publishOptions.click()

                self.publishNowButton = self.locateElement("//div[contains(text(), 'Publish now')]")
                self.schedule = self.locateElement("//div[contains(text(), 'Schedule')]")

                if publishNow == True:
                        self.publishNowButton.click()
                        self.playlist = self.locateElement("//span[contains(text(), 'Choose playlist(s)')]")
                        self.playlist.click()
                        try:
                                self.playlistSelect = self.locateElement(f"//div[contains(text(), '{playlistName}')]")
                        except:
                                raise Exception("Playlist not found")
                        self.playlistSelect.click()
                        
                        self.publishButton = self.locateElement("//div[contains(text(), 'Publish') and not(contains(text(), 'You') or contains(text(), 'now') or contains(text(), 'Options'))]")
                        while True:

                                try:
                                        self.uploadBar = self.locateElement("//div[contains(text(), 'Video Uploaded')]")
                                        self.publishButton.click()
                                        time.sleep(3.5)
                                        self.driver.close()
                                        break
                                except:
                                        time.sleep(2)
                                
                                        
                                
                                        



def upload_video(context):
        uploader = facebookVideoUpload()
        uploader.login("erick_kamyla@hotmail.com","unavacavestidadeuniforme")
        pageName = context['page']['Nombre']
        uploader.startUpload(context['video_path'],pageName)
        randomDescription = random.choice(context['page']['description'])
        if context['page']['thumbnail'] == True:
                uploader.title_description_tags(title=context['post'].title,description=randomDescription,tags=context['page']['tags'])
                uploader.addThumbnail(context["thumbnail_path"])
        else:
               uploader.title_description_tags(title="No creeras lo que pasó!",description=randomDescription,tags=context['page']['tags']) 
        uploader.publishVideo(playlistName=context['page']['playlist'])