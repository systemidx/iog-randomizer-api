using System.IO;

namespace Randomizer.Api.Configuration
{
    public class RandomizerConfiguration
    {
        public string TempStorageDestination
        {
            get
            {
                var dir = $@"{Path.GetTempPath()}\IOGR";
                if (!Directory.Exists(dir))
                    Directory.CreateDirectory(dir);

                return dir;
            }
        }
    }
}
