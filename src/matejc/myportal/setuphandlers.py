from plone import api

__docformat__ = "epytext"


def runCustomCode(site):
    """ Run custom add-on product installation code
    to modify Plone site object and others

    @param site: Plone site
    """
    if not api.group.get(groupname="staff"):
        api.group.create(
            groupname="staff",
            roles=['Reader'],
        )

    blogs_folder = api.content.get(path="/blogs")

    #if blogs_folder:                        # TODO: FOR DEBUG ONLY!!
    #    print "deleting blogs folder to re-add it"
    #    api.content.delete(blogs_folder)
    #    blogs_folder = None

    if not blogs_folder:
        blogs_folder = api.content.create(
            type="Folder",
            id="blogs",
            container=site,
        )
        myblog_folder = api.content.create(
            type="Folder",
            id="myblog",
            container=blogs_folder,
        )
        api.content.create(
            type="News Item",
            id="myblogentry",
            container=myblog_folder
        )

    # grant roles right after creation of context
    api.group.grant_roles(
        groupname="staff",
        obj=site["blogs"],
        roles=['Reader', 'Contributor', 'Editor', 'Reviewer'],
    )

    try:
        assert api.content.get(path="/collectmyblog")
    except:
        api.content.create(
            type="Collection",
            id="collectmyblog",
            container=site
        )
        myblog_coll = api.content.get(path="/collectmyblog")
        query = [
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': 'News Item',
            },
            {
                'i': 'path',
                'o': 'plone.app.querystring.operation.string.path',
                'v': '/blogs/myblog',
            }
        ]
        myblog_coll.setQuery(query)

        #myblog_coll.setExcludeFromNav(True)

    blogs_folder.setExcludeFromNav(True)


def setupVarious(context):
    """
    @param context:
        Products.GenericSetup.context.DirectoryImportContext instance
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('matejc.myportal.marker.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()

    runCustomCode(portal)
