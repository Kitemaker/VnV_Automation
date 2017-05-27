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
                        {
                            attr.Value = txtPrjName.Text;
                        }
                        if (attr.Name == "project_baseline")
                        {
                            attr.Value = txtPrjBline.Text;
                        }
                        if (attr.Name == "uevol_baseline")
                        {
                            attr.Value = txtUevolBline.Text;
                        }
                        if (attr.Name == "sydb_version")
                        {
                            attr.Value = txtdbBline.Text;
                        }
                        if (attr.Name == "sydt_version")
                        {
                            attr.Value = txtSyDTVer.Text;
                        }
                    }
                    SaveFileDialog dlg = new SaveFileDialog();
                    dlg.Filter = "DTVT Blue Project (*.dtprj)|*.dtprj";
                    dlg.DefaultExt = ".dtprj";
                    dlg.ValidateNames = true;
                    if (dlg.ShowDialog() == true)
                    {
                        newProjFilePath = dlg.FileName;
                        xdoc.GetElementsByTagName("RootFolder")[0].Attributes["path"].Value = new System.IO.FileInfo(newProjFilePath).DirectoryName;
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
