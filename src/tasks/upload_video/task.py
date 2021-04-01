
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pyautogui,time,random



class  facebookVideoUpload:
        def __init__(self) -> None:
                self.driver = webdriver.Firefox(executable_path="C:\\Users\\Erick\\projects\\auddit_extension\\bin\\geckodriver.exe")
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
                self.upload_video_button = self.locateElement("/html/body/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div[2]/div[3]/div/div[1]/div")
                self.upload_video_button.click()

                self.upload_single_video = self.locateElement("/html/body/div[1]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div[1]/div/div/ul/li[1]")
                self.upload_single_video.click()
                time.sleep(1)
                pyautogui.write(videopath)
                time.sleep(2)
                pyautogui.press('enter')
                
                self.pages_list = self.locateElements("/html/body/div[5]/div/div/div/div[1]/div/div[2]/div/div[2]/div/*/div/div/div/span/div")
                for page in self.pages_list:
                        if page.text == pageName:
                                page.click()
                                break
        def title_description_tags(self,title,description,tags):
                self.title_text = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div[2]/label/input")
                self.description_text = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div/div[2]/div")
                self.tags_text = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div[1]/div/div[2]/div/span[2]/label/input")
                
                self.title_text.send_keys(title)
                self.description_text.send_keys(description)
                for tag in tags:
                        self.tags_text.send_keys(tag)
                        time.sleep(2)
                        self.tags_text.send_keys(Keys.ARROW_UP)
                        self.tags_text.send_keys(Keys.RETURN)
                        time.sleep(2)
        def addThumbnail(self,thumbnailPath):
                self.thumbnailButton = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]")
                self.thumbnailButton.click()

                self.addImageButton = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div[2]/a/div")
                self.addImageButton.click()
                time.sleep(1)
                pyautogui.write(thumbnailPath)
                time.sleep(2)
                pyautogui.press('enter')

        def publishVideo(self,publishNow=True,date=None):
                self.publishOptions = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div")
                self.publishOptions.click()

                self.publishNowButton = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div[1]/div")
                self.schedule = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div[2]/div")

                if publishNow == True:
                        self.publishNowButton.click()
                        self.playlist = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div/div/div[3]/div[3]/div[2]")
                        self.playlist.click()
                        try:
                                self.playlistSelect = self.locateElement("/html/body/div[8]/div/div/div/div/div/div[1]/div/div/ul/li[1]/div")
                        except:
                                try:
                                        self.playlistSelect = self.locateElement("/html/body/div[9]/div/div/div/div/div/div[1]/div/div/ul/li[1]/div")
                                except:
                                        raise Exception("Playlist not found")
                        self.playlistSelect.click()
                        self.uploadBar = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[3]/div[1]/div[1]/div/div/div[2]")
                        self.publishButton = self.locateElement("/html/body/div[5]/div/div/div/div[2]/div/div/div[3]/div[2]/a[2]")
                        while True:
                                if self.uploadBar.text == "Video Uploaded":
                                        self.publishButton.click()
                                        time.sleep(3.5)
                                        self.driver.close()
                                        break
                                else:
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
        uploader.publishVideo()