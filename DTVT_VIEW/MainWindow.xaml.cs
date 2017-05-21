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
        internal string projSyDBFilePath = string.Empty;
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
            ReadProjectFile(projFile);
            FillTextBoxes();
            if (projCsvFolderPath != string.Empty)
            {
                LoadCsvFiles(projCsvFolderPath);
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
                foreach (XmlNode node in docNode.ChildNodes)
                {
                    switch (node.Name)
                    {
                        case "Project_Baseline":
                            projBaseline = node.InnerText;
                            break;
                        case "Uevol_Baseline":
                            uevolBaseline = node.InnerText;
                            break;
                        case "Database_Baseline":
                            dbBaseline = node.InnerText;
                            break;
                        case "SyDT_Version":
                            sydtVersion = node.InnerText;
                            break;
                        case "RootFolder":
                            projRootFolder = node.InnerText;
                            break;
                        case "ConstantFile":
                            projConstantFilePath = node.InnerText;
                            break;
                        case "SyDBFile":
                            projSyDBFilePath = node.InnerText;
                            break;
                        case "CsvFolder":
                            projCsvFolderPath = node.InnerText;
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

        private void WndMain_Closing(object sender, System.ComponentModel.CancelEventArgs e)
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
                    }
                }
                catch (Exception ex)
                { System.Windows.Forms.MessageBox.Show(ex.Message); }
            }
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
                projectXmlDoc.GetElementsByTagName("RulesFolder")[0].InnerText = dlg.SelectedPath;
                LoadRules(dlg.SelectedPath);
            }

        }

        private void LoadCsvFiles(string CsvFoderPath)
        {
            System.IO.DirectoryInfo csvDir = new DirectoryInfo(CsvFoderPath);
            foreach (FileInfo finfo in csvDir.GetFiles("*.csv", SearchOption.TopDirectoryOnly))
            {
                listCsvFiles.Items.Add(finfo.Name);
            }

        }
        private void dataMenu_Click(object sender, RoutedEventArgs e)
        {
            FolderBrowserDialog dlg = new FolderBrowserDialog();
            if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                projCsvFolderPath = dlg.SelectedPath;
                projectXmlDoc.GetElementsByTagName("CsvFolder")[0].InnerText = dlg.SelectedPath;
                LoadCsvFiles(dlg.SelectedPath);
            }
        }

        private void LoadRules(string RuleFolderPath)
        {
            System.IO.DirectoryInfo csvDir = new DirectoryInfo(RuleFolderPath);
            foreach (FileInfo finfo in csvDir.GetFiles("*.py", SearchOption.TopDirectoryOnly))
            {
                this.listRules.Items.Add(finfo.Name);
            }

        }

        private void constMenu_Click(object sender, RoutedEventArgs e)
        {
            FolderBrowserDialog dlg = new FolderBrowserDialog();
            if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                projConstantFilePath = dlg.SelectedPath;
                projectXmlDoc.GetElementsByTagName("ConstantFolder")[0].InnerText = dlg.SelectedPath;
            }
        }

      
    }
}
