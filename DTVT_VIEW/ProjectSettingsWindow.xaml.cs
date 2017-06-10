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
using System.Windows.Shapes;
using System.IO;
using System.Windows.Forms;

namespace DTVT_VIEW
{
    /// <summary>
    /// Interaction logic for ProjectSettingsWindow.xaml
    /// </summary>
    public partial class ProjectSettingsWindow : Window
    {
        string _rulesPath;
        string _dataPath;
        string _sydbPath;
        string _constPath;

        public ProjectSettingsWindow()
        {
            InitializeComponent();
        }

        private void btnImportRule_Click(object sender, RoutedEventArgs e)
        {
            FolderBrowserDialog dlg = new FolderBrowserDialog();
            if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                _rulesPath = dlg.SelectedPath;
                txtImportRule.Text = dlg.SelectedPath;

            }

        }
        #region Properties
        public string RulesPath
        {
            get
            {
                return _rulesPath;
            }
            set
            {
                _rulesPath = value;
            }
        }
        public string DataPath
        {
            get
            {
                return _dataPath;
            }
            set
            {
                _dataPath = value;
            }
        }
        public string SyDBPath
        {
            get
            {
                return _sydbPath;
            }
            set
            {
                _sydbPath = value;
            }
        }
        public string ConstantPath
        {
            get
            {
                return _constPath;
            }
            set
            {
                _constPath = value;
            }
        }
        #endregion

        private void btnImportData_Click(object sender, RoutedEventArgs e)
        {
            FolderBrowserDialog dlg = new FolderBrowserDialog();
            if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                _dataPath = dlg.SelectedPath;
                txtImportData.Text = dlg.SelectedPath;

            }
        }

        private void btnImportSydb_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                FolderBrowserDialog dlg = new FolderBrowserDialog();
                if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    _sydbPath = dlg.SelectedPath;
                    txtImportSydb.Text = dlg.SelectedPath;
                    
                }
            }
            catch (Exception ex)
            {
                System.Windows.Forms.MessageBox.Show(ex.Message);
            }
        }

        private void btnImportConst_Click(object sender, RoutedEventArgs e)
        {
            FolderBrowserDialog dlg = new FolderBrowserDialog();
            if (dlg.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                _constPath = dlg.SelectedPath;
                txtImportConst.Text = dlg.SelectedPath;

            }
        }

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {

        }

        private void btnCancel_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
    }
}
