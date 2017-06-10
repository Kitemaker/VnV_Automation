using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Diagnostics;
using System.Configuration;

using System.Xml;
using System.IO;
using System.Windows.Forms;

namespace DTVT_VIEW
{

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    

    public partial class MainWindow : Window
    {
        bool projLoaded = false;
        DTVT_VIEW.NewProject _newProj;
        public string projFile = string.Empty;
        string projName = string.Empty;
        string projBaseline = string.Empty;
        string uevolBaseline = string.Empty;
        string dbBaseline = string.Empty;
        string sydtVersion = string.Empty;
        string projRootFolder = string.Empty;
        string projConstantFilePath = string.Empty;
        string projCsvFolderPath = string.Empty;
        string projRulesFolderPath = string.Empty;
        string projConstantFolder = string.Empty;
        string projRulesFolder = string.Empty;
        string projSyDBFilePath = string.Empty;
        private DirectoryInfo rulesDir = null;
        string rootFolder = string.Empty;
        string pythonPath = string.Empty;
        XmlDocument projectXmlDoc;
        ProjectSettingsWindow projSettingWnd;
        
        

        public MainWindow()
        {
            InitializeComponent();
            InitialiseData();
            EnableProjectTextBox(false);
        }


        private void InitialiseData()
        {
            rootFolder = System.IO.Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
            pythonPath = ConfigurationManager.AppSettings["python"];            

        }
        private void newPrjMenu_Click(object sender, RoutedEventArgs e)
        {
            _newProj = new DTVT_VIEW.NewProject();
            _newProj.Closing += _newProj_Closing;
            _newProj.Tag = this;
            _newProj.Show();
        }

        private void _newProj_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            projFile = _newProj.newProjFilePath;
            if (System.IO.File.Exists(projFile))
            {
                ReadProjectFile(projFile);
                FillTextBoxes();
                if (txtPrjName.Text != string.Empty)
                {
                    projLoaded = true;
                    lboxOutput.Items.Add(DateTime.Now.ToString() + "\t" + "Project " + txtPrjName + " has been loaded successfully.");
                }
            }
        }

        private void EnableProjectTextBox(bool enableValue)
        {
            txtPrjName.IsEnabled = enableValue;
            txtdbBline.IsEnabled = enableValue;
            txtPrjBline.IsEnabled = enableValue;
            txtSyDTVer.IsEnabled = enableValue;
            txtUevolBline.IsEnabled = enableValue;
        }

        private void openPrjMenu_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog _dlg = new OpenFileDialog();
            _dlg.Filter = "DTVT Blue Project (*.dtprj)|*.dtprj";
            _dlg.Multiselect = false;
            DialogResult _res = _dlg.ShowDialog();
            if (_res == System.Windows.Forms.DialogResult.OK)
            {
                projFile = _dlg.FileName;
            }
            try
            {
                ReadProjectFile(projFile);
                FillTextBoxes();
                projLoaded = true;
                lboxOutput.Items.Add(DateTime.Now.ToString() + "\t" + "Project " + txtPrjName + " has been loaded successfully.");
            }
            catch (Exception ex)
            {
                projLoaded = false;
                System.Windows.Forms.MessageBox.Show("Error Loading project file :\t" + projFile + "\n" + "Source:\t openPrjMenu_Click");
            }
            if (projCsvFolderPath != string.Empty)
            {
                LoadCsvFiles(projCsvFolderPath);
            }
            if (projRulesFolder != string.Empty)
            {
               LoadRules(projRulesFolder);
               
            }


        }

        private void ReadProjectFile(string filename)
        {
            XmlElement docNode;
            if (System.IO.File.Exists(filename))
            {
                projectXmlDoc = new XmlDocument();
                projectXmlDoc.Load(filename);
                docNode = projectXmlDoc.DocumentElement;
                projName = docNode.GetAttribute("name");
                projBaseline = docNode.GetAttribute("project_baseline");
                uevolBaseline = docNode.GetAttribute("uevol_baseline");
                sydtVersion = docNode.GetAttribute("sydt_version");
                dbBaseline = docNode.GetAttribute("sydb_version");
                foreach (XmlNode node in docNode.ChildNodes)
                {
                    switch (node.Name)
                    {          
                        case "RootFolder":
                            projRootFolder = node.Attributes["path"].Value;
                            break;
                        case "ConstantFile":
                            projConstantFilePath = node.Attributes["path"].Value;
                            break;
                        case "SyDBFile":
                            projSyDBFilePath = node.Attributes["path"].Value;
                            break;
                        case "CsvFolder":
                            projCsvFolderPath = node.Attributes["path"].Value;
                            break;
                        case "RulesFolder":
                            projRulesFolder = node.Attributes["path"].Value;
                            break;
                        default:
                            break;
                    }
                }
            }


        }

        private void FillTextBoxes()
        {
            txtPrjBline.Text = projBaseline;
            txtdbBline.Text = dbBaseline;
            txtPrjName.Text = projName;
            txtSyDTVer.Text = sydtVersion;
            txtUevolBline.Text = uevolBaseline;

        }

        private void ClearTextBoxes()
        {
            txtPrjBline.Text = string.Empty;
            txtdbBline.Text = string.Empty;
            txtPrjName.Text = string.Empty;
            txtSyDTVer.Text = string.Empty;
            txtUevolBline.Text = string.Empty;
        }

        private void WndMain_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            SaveProjectFile();
        }


        private void exitPrjMenu_Click(object sender, RoutedEventArgs e)
        {
            DialogResult res = System.Windows.Forms.MessageBox.Show("Do you want to exit?", "", MessageBoxButtons.YesNo, MessageBoxIcon.Question, MessageBoxDefaultButton.Button2);
            if (res == System.Windows.Forms.DialogResult.Yes)
            {
                this.Close();
            }
        }

        private void rulesMenu_Click(object sender, RoutedEventArgs e)
        {
            FolderBrowserDialog dlg = new FolderBrowserDialog();
            if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                projRulesFolderPath = dlg.SelectedPath;
                projectXmlDoc.GetElementsByTagName("RulesFolder")[0].Attributes["path"].Value = dlg.SelectedPath;
                LoadRules(dlg.SelectedPath);
            }

        }
        private void LoadRules(string RuleFolderPath)
        {
            rulesDir = new DirectoryInfo(RuleFolderPath);
            foreach (FileInfo finfo in rulesDir.GetFiles("*.py", SearchOption.TopDirectoryOnly))
            {
                this.listRules.Items.Add(finfo.Name);
            }

        }

        private void dataMenu_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                FolderBrowserDialog dlg = new FolderBrowserDialog();
                if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    projCsvFolderPath = dlg.SelectedPath;
                    projectXmlDoc.GetElementsByTagName("CsvFolder")[0].Attributes["path"].Value = dlg.SelectedPath;
                    LoadCsvFiles(dlg.SelectedPath);
                }
            }
            catch (Exception ex)
            {
                System.Windows.Forms.MessageBox.Show(ex.Message);
            }
        }


        private void LoadCsvFiles(string CsvFoderPath)
        {
            try
            {
                System.IO.DirectoryInfo csvDir = new DirectoryInfo(CsvFoderPath);
                foreach (FileInfo finfo in csvDir.GetFiles("*.csv", SearchOption.TopDirectoryOnly))
                {
                    listCsvFiles.Items.Add(finfo.Name);
                }
            }
            catch (Exception ex)
            { System.Windows.Forms.MessageBox.Show(ex.Message); }

        }    

        private void constMenu_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                FolderBrowserDialog dlg = new FolderBrowserDialog();
                if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    projConstantFilePath = dlg.SelectedPath;
                    projectXmlDoc.GetElementsByTagName("ConstantFolder")[0].Attributes["path"].Value = dlg.SelectedPath;
                }
            }
            catch (Exception ex)
            {
                System.Windows.Forms.MessageBox.Show(ex.Message);
            }
        }        

        private void listRules_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            FileInfo finfo = new FileInfo(rulesDir.FullName + "\\" + listRules.SelectedValue.ToString());
            StreamReader fstream = finfo.OpenText();

            tblockRule.Text = "";
            tblockRule.Text = fstream.ReadToEnd();
        }

        private void ruleContMenuVerify_Click(object sender, RoutedEventArgs e)
        {
            FileInfo finfo = new FileInfo(rulesDir.FullName + "\\" + listRules.SelectedValue.ToString());
            VerifyRule(finfo.FullName);
            
        }

        private void importMenu_SubmenuOpened(object sender, RoutedEventArgs e)
        {
            if (txtPrjName.Text == string.Empty)
            {
                foreach (ItemsControl menu in importMenu.Items)
                {
                    menu.IsEnabled = false;

                }
            }
            else
            {
                foreach (ItemsControl menu in importMenu.Items)
                {
                    menu.IsEnabled = true;

                }
            }
        }

        private void savePrjMenu_Click(object sender, RoutedEventArgs e)
        {
            SaveProjectFile();
        }

        private void SaveProjectFile()
        {

            XmlDocument existingFile = new XmlDocument();
            if (projFile != string.Empty && existingFile != null)
            {
                try
                {
                    existingFile.Load(projFile);
                    if (existingFile.DocumentElement.InnerXml != projectXmlDoc.DocumentElement.InnerXml)
                    {
                        projectXmlDoc.Save(projFile);
                        lboxOutput.Items.Add(DateTime.Now.ToString() + "\t" + "Project file " + projFile + " has been saved successfully.");
                    }
                    
                }
                catch (Exception ex)
                { System.Windows.Forms.MessageBox.Show(ex.Message); }
            }


        }

        private void sydbMenu_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                FolderBrowserDialog dlg = new FolderBrowserDialog();
                if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    projConstantFilePath = dlg.SelectedPath;
                    projectXmlDoc.GetElementsByTagName("SyDBFile")[0].Attributes["path"].Value = dlg.SelectedPath;
                }
            }
            catch (Exception ex)
            {
                System.Windows.Forms.MessageBox.Show(ex.Message);
            }

        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="PythonScript">Full path of Python Script</param>
        private void VerifyRule(string PythonScript)
        {
            if (pythonPath == string.Empty)
            {
               System.Windows.Forms.MessageBox.Show("Python Exe path is not set\n");
                return;
            }
            if (rootFolder == string.Empty)
            {
                System.Windows.Forms.MessageBox.Show("Root Folder path is not \n");
                return;
            }

            string outString;
            // Create new process start info 
            ProcessStartInfo myProcessStartInfo = new ProcessStartInfo(pythonPath);

            // make sure we can read the output from stdout 
            myProcessStartInfo.UseShellExecute = false;
            myProcessStartInfo.RedirectStandardOutput = true;

            // start python app with 3 arguments  
            // 1st arguments is pointer to itself,  
            // 2nd and 3rd are actual arguments we want to send 
            myProcessStartInfo.Arguments =   PythonScript  + " " + rootFolder;

            Process myProcess = new Process();
            // assign start information to the process 
            myProcess.StartInfo = myProcessStartInfo;
            
            lboxOutput.Items.Add(DateTime.Now.ToString() + "\t" + "Calling Python script with arguments "+ PythonScript + " , "+ rootFolder);
            
            // start the process 
            myProcess.Start();

            // Read the standard output of the app we called.  
            // in order to avoid deadlock we will read output first 
            // and then wait for process terminate: 
            StreamReader myStreamReader = myProcess.StandardOutput;
            string myString = myStreamReader.ReadLine();

            /*if you need to read multiple lines, you might use: 
                string myString = myStreamReader.ReadToEnd() */

            // wait exit signal from the app we called and then close it. 
            myProcess.WaitForExit();
            myProcess.Close();

            // write the output we got from python app 
            lboxOutput.Items.Add(DateTime.Now.ToString() + "\t"+ myString);



        }

        private void setPython_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog _dlg = new OpenFileDialog();
            _dlg.Filter = "DTVT Blue Project (*.exe)|*.exe";
            _dlg.Multiselect = false;
            DialogResult _res = _dlg.ShowDialog();
            if (_res == System.Windows.Forms.DialogResult.OK)
            {
                try
                {
                    ConfigurationManager.AppSettings["python"] = _dlg.FileName;
                    var configFile = ConfigurationManager.OpenExeConfiguration(ConfigurationUserLevel.None);
                    var settings = configFile.AppSettings.Settings;
                    settings["python"].Value = _dlg.FileName;
                    configFile.Save(ConfigurationSaveMode.Modified);
                    ConfigurationManager.RefreshSection(configFile.AppSettings.SectionInformation.Name);
                    pythonPath = ConfigurationManager.AppSettings["python"];
                }
                 
                catch (ConfigurationErrorsException)
                {
                    System.Windows.Forms.MessageBox.Show("Error writing app settings");
                }
            }
           
        }

        private void importMenu_Click(object sender, RoutedEventArgs e)
        {

        }

        private void settingsMenu_Click(object sender, RoutedEventArgs e)
        {
            projSettingWnd = new ProjectSettingsWindow();
            projSettingWnd.ShowDialog();
        }

      
    }
}
