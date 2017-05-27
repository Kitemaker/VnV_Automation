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
        XmlDocument projectXmlDoc;

        public MainWindow()
        {
            InitializeComponent();
            EnableProjectTextBox(false);
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
            System.Windows.Forms.MessageBox.Show("Do you want to run rule:\n" + finfo.FullName);
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

   
    }
}
