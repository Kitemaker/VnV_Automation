using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Xml;
using Microsoft.Win32;


namespace DTVT_VIEW
{
    /// <summary>
    /// Interaction logic for winNewProject.xaml
    /// </summary>
    public partial class NewProject : Window
    {
        bool dataChanged = false;
        public string newProjFilePath = string.Empty;
        MainWindow _parent;
        public NewProject()
        {
            InitializeComponent();
            btnSave.IsEnabled = false;
            _parent = (MainWindow)this.Tag;
        }

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                System.Text.RegularExpressions.Regex regex = null;
                regex = new System.Text.RegularExpressions.Regex("^([a-zA-Z0-9])*$");

                if (String.IsNullOrEmpty(txtPrjName.Text))
                {
                    MessageBox.Show("Invalid Project Name. Project Name cannot be empty.");
                    return;
                }                

                if (regex.IsMatch(txtPrjName.Text))
                {

                    XmlDocument xdoc = new XmlDocument();
                    xdoc.Load("New_Project_Template.xml");

                    foreach (XmlAttribute attr in xdoc.DocumentElement.Attributes)
                    {
                        if (attr.Name == "name")
                        { attr.Value = txtPrjName.Text; }
                    }
                    SaveFileDialog dlg = new SaveFileDialog();
                    dlg.Filter = "DTVT Blue Project (*.dtprj)|*.dtprj";
                    dlg.DefaultExt = ".dtprj";
                    dlg.ValidateNames = true;
                    if (dlg.ShowDialog() == true)
                    {
                        newProjFilePath = dlg.FileName;
                        WriteProjectFile(xdoc);
                        xdoc.Save(dlg.FileName);
                    }                  
                }
                else
                {
                    MessageBox.Show("Invalid password. Password cannot contain any special characters.");
                    return;
                }

                this.Close();
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
           
        }

        private void WriteProjectFile(XmlDocument xdoc)
        {   
            xdoc.GetElementsByTagName("Project_Baseline")[0].InnerText = this.txtPrjBline.Text;
            xdoc.GetElementsByTagName("Uevol_Baseline")[0].InnerText = this.txtUevolBline.Text;
            xdoc.GetElementsByTagName("Database_Baseline")[0].InnerText = this.txtdbBline.Text;
            xdoc.GetElementsByTagName("SyDT_Version")[0].InnerText = this.txtSyDTVer.Text;
            xdoc.GetElementsByTagName("RootFolder")[0].InnerText = new System.IO.FileInfo(newProjFilePath).DirectoryName;
           
        }


         

        private void btnCancel_Click(object sender, RoutedEventArgs e)
        {
            this.Close();

        }

        private void txtPrjName_TextChanged(object sender, TextChangedEventArgs e)
        {
            dataChanged = true;
            btnSave.IsEnabled = true;

        }

        private void txtPrjBline_TextChanged(object sender, TextChangedEventArgs e)
        {
            btnSave.IsEnabled = true;
        }

        private void txtUevolBline_TextChanged(object sender, TextChangedEventArgs e)
        {
            btnSave.IsEnabled = true;
        }

        private void txtdbBline_TextChanged(object sender, TextChangedEventArgs e)
        {
            btnSave.IsEnabled = true;
        }

        private void txtSyDTVer_TextChanged(object sender, TextChangedEventArgs e)
        {
            btnSave.IsEnabled = true;
        }

        private void txtPrjName_KeyDown(object sender, KeyEventArgs e)
        {
           
        }

       
    }
}
